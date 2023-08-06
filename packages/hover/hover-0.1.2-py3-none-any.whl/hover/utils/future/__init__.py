import torch 
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import spacy
import copy
from tqdm import tqdm
from torch.utils.data import Dataset
from snorkel.classification import cross_entropy_with_probs
from collections import defaultdict

DEFAULT_NLP = spacy.load('en_vectors_web_lg') # be sure not to use 'core' if you only need vectors. The running time can be different by a factor of ~ 20 to 100.
def default_doc2vec(text):
    return DEFAULT_NLP(text).vector

class TextDataset(Dataset):
    '''
    Torch Dataset of labeled text.
    '''
    def __init__(self, texts, labels, doc2vec=default_doc2vec):
        '''
        Initialize the dataset.
        '''
        assert len(texts) == len(labels)
        self.texts = texts[:]
        self.labels = labels[:]
        self.vectors = []
        for _text in tqdm(self.texts):
            self.vectors.append(doc2vec(_text))

    def __getitem__(self, index):
        '''
        Get the piece of data corresponding to a specified index.
        '''
        return self.vectors[index], self.labels[index], index

    def __len__(self):
        return len(self.texts)

def loss_coteaching(y_1, y_2, t, forget_rate):
    '''
    Deprecated.
    '''
    loss_1 = cross_entropy_with_probs(y_1, t, reduction='none')
    ind_1_sorted = np.argsort(loss_1.data)
    loss_1_sorted = loss_1[ind_1_sorted]

    loss_2 = cross_entropy_with_probs(y_2, t, reduction='none')
    ind_2_sorted = np.argsort(loss_2.data)
    loss_2_sorted = loss_2[ind_2_sorted]

    remember_rate = 1 - forget_rate
    num_remember = int(remember_rate * len(loss_1_sorted))
    assert num_remember > 0

    ind_1_update=ind_1_sorted[:num_remember]
    ind_2_update=ind_2_sorted[:num_remember]
    # exchange
    loss_1_update = cross_entropy_with_probs(y_1[ind_2_update], t[ind_2_update], reduction='mean')
    loss_2_update = cross_entropy_with_probs(y_2[ind_1_update], t[ind_1_update], reduction='mean')

    return torch.sum(loss_1_update)/num_remember, torch.sum(loss_2_update)/num_remember

def loss_coteaching_directed(y_student, y_teacher, target, forget_rate):
    '''
    Subroutine for loss_coteaching_graph.
    '''
    import math
    num_remember = math.ceil((1 - forget_rate) * target.size(0))
    assert num_remember > 0

    loss_teacher_detail = cross_entropy_with_probs(y_teacher, target, reduction='none')
    idx_to_learn = np.argsort(loss_teacher_detail.data)[:num_remember]
    loss_student = cross_entropy_with_probs(y_student[idx_to_learn], target[idx_to_learn], reduction='mean').unsqueeze(0)
    return loss_student

def get_disagreement(y_list, reduce=False):
    '''
    Compute disagreements between predictions given bylogits.
    '''
    pred_list = [torch.argmax(_y.data, dim=1).numpy() for _y in y_list]
    disagreement = defaultdict(dict)
    for i in range(0, len(pred_list)):
        for j in range(i, len(pred_list)):
            _disagreed = np.not_equal(pred_list[i], pred_list[j])
            if reduce:
                _disagreed = np.mean(_disagreed)
            disagreement[i][j] = _disagreed 
            disagreement[j][i] = _disagreed
    return dict(disagreement)

def loss_coteaching_graph(y_list, target, forget_rate, tail_head_adjacency_list, disagree_mode=True):
    '''
    Co-teaching from differences.
    Generalized to graph representation where each vertex is a classifier and each edge is a source to check differences with and to learn from.
    y_list -- list of logits from different classifiers.
    t -- target, which is allowed to be probabilistic.
    forget_rate -- the proportion of high-loss contributions to discard.
    tail_head_adjacency_list -- the 'tail' classifier learns from the 'head'.
    '''
    # pre-compute disagreements that get used repeatedly later
    disagree_indexes = get_disagreement(y_list, reduce=False)

    # initialize co-teaching losses
    loss_list = []
    for i in range(0, len(y_list)):
        assert tail_head_adjacency_list[i]
        _losses = []
        for j in tail_head_adjacency_list[i]:
            # learn from disagreement
            if np.any(disagree_indexes[i][j]) and disagree_mode:
                # PyTorch Tensor comprehension: need to cast boolean np.array to list
                y_student = F.softmax(y_list[i], dim=1)[disagree_indexes[i][j].tolist()]
                y_teacher = F.softmax(y_list[j], dim=1)[disagree_indexes[i][j].tolist()]
                _contribution = loss_coteaching_directed(y_student, y_teacher, target[disagree_indexes[i][j].tolist()], forget_rate)
            else:
                # if no disagreement, fall back to vanilla coteaching
                _contribution = loss_coteaching_directed(y_list[i], y_list[j], target, forget_rate)
            # add loss contribution to list
            _losses.append(_contribution)
        # concatenate and average up
        _loss = torch.mean(torch.cat(_losses))
        loss_list.append(_loss)
    return loss_list

def get_two_stage_params(base_lr, first_stage_momentum, first_stage_epochs,
                         base_fr, second_stage_momentum, second_stage_epochs):
    '''
    Specify two-stage training parameters.
    '''
    learning_rates = [base_lr] * first_stage_epochs + [base_lr * _coeff for _coeff in np.linspace(1.0, 0.0, second_stage_epochs)]

    forget_rates = [base_fr * _coeff for _coeff in np.linspace(0.0, 1.0, first_stage_epochs)] + [base_fr] * second_stage_epochs

    momenta = [first_stage_momentum] * first_stage_epochs + [second_stage_momentum] * second_stage_epochs
    return list(zip(learning_rates, forget_rates, momenta))

def get_loaders(X, y, batch_size=128):
    '''
    Example:
    X: {'train': [texts], 'dev': [texts], 'test': [texts]}
    y: {'train': [labels], 'dev': [labels], 'test': [labels]}
    '''
    loaders = dict()
    for _dataset_name, texts in X.items():
        labels = y.get(_dataset_name)
        dataset = TextDataset(texts, labels)
        loaders[_dataset_name] = torch.utils.data.DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True, drop_last=False)
    return loaders

def accuracy(logits, target):
    pred = F.softmax(logits, dim=1).argmax(dim=1)
    true = target.argmax(dim=1)
    batch_size = target.size(0)
    correct = int(pred.eq(true).sum())
    return float(correct) / float(batch_size)

class CoteachingClassifier(object):
    '''
    Implementation of the co-teaching framework.
    '''
    def __init__(self, models, optimizers):
        '''
        Initializer. [more description to be added]
        '''
        assert len(models) == len(optimizers)
        self.models = models
        self.optimizers = optimizers
        self._dynamic_params = dict()
        self._tracker = {'accuracy': [0] * len(self.models)}
        self.snapshot = dict()
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.no_gains = 0

    def update_snapshot(self, acc):
        '''
        Snapshot the models at their best dev accuracy.
        '''
        updated = False
        for i in range (0, len(self.models)):
            acc_key = 'acc{0}'.format(i)
            model_key = 'model{0}'.format(i)
            if acc[i] > self.snapshot.get(acc_key, 0.0):
                self.snapshot[acc_key] = acc[i]
                self.snapshot[model_key] = copy.deepcopy(self.models[i])
                updated = True
        return updated

    def early_stop(self, updated, patience, conditions=[]):
        '''
        Determine whether to terminate training.
        '''
        assert isinstance(patience, int) and patience > 1
        for _condition in conditions:
            if not bool(_condition):
                return False
        if bool(updated):
            self.no_gains = 0
            return False
        else:
            self.no_gains += 1
        if self.no_gains > patience:
            return True
        return False

    def train(self, train_loader, epoch_params, dev_loader, patience=30, teacher_adjacency_function=None, verbose=1, disagree_mode=True, take_snapshots=True, freeze=[]):
        '''
        epoch_params -- list of (learning_rate, momentum, forget_rate) tuples.
        '''
        def compile_coteaching_scheme_info(teachers, disagreement):
            '''
            Compile a message that describes the co-teaching scheme.
            '''
            message = ""
            for i in range(0, len(teachers)):
                neighbors = teachers[i]
                for j in neighbors:
                    dis_ij = disagreement[i][j]
                    message += "\n {0: <100}".format("{student} <- {teacher}, disagreement={dis:.3f}".format(**{"student": i, "teacher": j, "dis": dis_ij}))
            return message

        for epoch_idx, (learning_rate, forget_rate, momentum) in enumerate(epoch_params):
            _teachers, disagreement_count = self.select_teachers(dev_loader, teacher_adjacency_function)
            if verbose > 1:
                print(compile_coteaching_scheme_info(_teachers, disagreement_count))
            self._dynamic_params['teachers'] = _teachers
            self._dynamic_params['epoch'] = epoch_idx + 1
            self._dynamic_params['lr'] = learning_rate
            self._dynamic_params['momentum'] = momentum
            self._dynamic_params['forget_rate'] = forget_rate
            self.adjust_params()
            self.train_epoch(train_loader, verbose=verbose, disagree_mode=disagree_mode, freeze=freeze)
            acc_list = self.evaluate(dev_loader, self.models, verbose=verbose)
            self._tracker['accuracy'] = acc_list
            if take_snapshots:
                updated = self.update_snapshot(acc_list)
                if self.early_stop(updated, patience):
                    print('Early stop is triggered.')
                    break

    def adjust_params(self):
        '''
        Update dynamics paramaters in the optimizer.
        '''
        for _opt in self.optimizers:
            for _group in _opt.param_groups:
                _group['lr'] = self._dynamic_params['lr']
                _group['betas'] = (self._dynamic_params['momentum'], 0.999)

    def evaluate(self, test_loader, eval_models, verbose=1):
        '''
        Evaluate individual models.
        '''
        # put models in eval mode
        for _model in eval_models:
            _model.eval()
        # calculate accuracy
        total = 0
        correct = [0] * len(eval_models)
        for loaded_input, loaded_output, _ in test_loader:
            input_tensor = loaded_input.float()
            output_tensor = loaded_output.float()
            total += output_tensor.size(0)
            for i, _model in enumerate(eval_models):
                logits = _model(input_tensor)
                batch_acc = accuracy(logits, output_tensor)
                correct[i] += output_tensor.size(0) * batch_acc
        overall_acc = [_num / total for _num in correct]
        if verbose > 0:
            log_info = dict(self._dynamic_params)
            log_info['acc'] = ''.join(['|M{0}: {1:.3f} '.format(i, _acc) for i, _acc in enumerate(overall_acc)])
            print("{0: <100}".format("Epoch {epoch} eval acc {acc}".format(**log_info)))
        return overall_acc

    def evaluate_combination(self, test_loader, eval_models):
        '''
        Add up logits from individual models and evaluate.
        '''
        # put models in eval mode
        for _model in eval_models:
            _model.eval()
        # calculate accuracy
        total = 0
        correct = 0
        for loaded_input, loaded_output, _ in test_loader:
            input_tensor = loaded_input.float()
            output_tensor = loaded_output.float()
            total += output_tensor.size(0)
            logits_cumulative = None
            for i, _model in enumerate(eval_models):
                logits = _model(input_tensor)
                if logits_cumulative is None:
                    logits_cumulative = logits
                else:
                    logits_cumulative = logits_cumulative.add(logits)
            batch_acc = accuracy(logits_cumulative, output_tensor)
            correct += output_tensor.size(0) * batch_acc
        overall_acc = correct / total
        log_info = dict(self._dynamic_params)
        log_info['acc'] = overall_acc
        print("{0: <100}".format("Epoch {epoch} combination-eval acc {acc}".format(**log_info)))
        return overall_acc

    def select_teachers(self, dev_loader, adjacency_function=None):
        '''
        Select teachers for each model.
        The strategy is to pick models that disagree the most and have accuracy above some bar.
        '''
        if adjacency_function is None:
            def default_adjacency_function(accuracy, disagreement, acc_bar=0.5):
                # initialize teachers
                teachers = []
                for i in range(0, len(self.models)):
                    candidates = [j for j in disagreement_count[i].keys() if accuracy[j] >= acc_bar and disagreement_count[i][j] > 0]
                    # if no suitable candidate or not yet suitable for cross-learning, reduce to vanilla training
                    if (not candidates) or accuracy[i] < acc_bar:
                        _teacher = [i]
                    else:
                        top_disagreers = sorted(candidates, key=lambda j: disagreement_count[i][j], reverse=True)
                        _teacher = top_disagreers[:1]
                    teachers.append(_teacher)
                return teachers
            adjacency_function = default_adjacency_function
        
        assert callable(adjacency_function)
        # compute logits over the entire dev set
        for _model in self.models:
            _model.eval()
        logits_dict = defaultdict(list)
        for loaded_input, _, _ in dev_loader:
            input_tensor = loaded_input.float()
            for i, _model in enumerate(self.models):
                logits = _model(input_tensor)
                logits_dict[i].append(logits)
        logits_list = []
        for _idx in sorted(logits_dict.keys()):
            logits_list.append(torch.cat(logits_dict[_idx]))

        disagreement_count = get_disagreement(logits_list, reduce=True)
        teachers = adjacency_function(self._tracker['accuracy'], disagreement_count)
        return teachers, disagreement_count

    def train_epoch(self, train_loader, verbose, disagree_mode, freeze):
        '''
        Train for one epoch.
        '''
        for i, _model in enumerate(self.models):
            if not i in freeze:
                _model.train()
        for batch_idx, (loaded_input, loaded_output, index) in enumerate(train_loader):
            self._dynamic_params['batch'] = batch_idx + 1
            self.train_batch(loaded_input, loaded_output, verbose=verbose, disagree_mode=disagree_mode, freeze=freeze)

    def train_batch(self, loaded_input, loaded_output, verbose, disagree_mode, freeze):
        '''
        Train for one batch.
        '''
        input_tensor = loaded_input.float()
        output_tensor = loaded_output.float()

        # compute logits
        logits_list = []
        acc_list = []
        for _model in self.models:
            _logits = _model(input_tensor)
            _acc = accuracy(_logits, output_tensor)
            logits_list.append(_logits)
            acc_list.append(_acc)

        # compute losses
        loss_list = loss_coteaching_graph(logits_list, output_tensor, self._dynamic_params['forget_rate'], self._dynamic_params['teachers'], disagree_mode=disagree_mode)
  
        # update weights
        for i, _opt in enumerate(self.optimizers):
            if not i in freeze:
                _opt.zero_grad()
                loss_list[i].backward()
                _opt.step()

        if verbose > 0:
            log_info = dict(self._dynamic_params)
            log_info['performance'] = ''.join(['|M{0}: L {1:.3f}'.format(i, _loss, _acc) for i, (_loss, _acc) in enumerate(zip(loss_list, acc_list))])
            print("{0: <100}".format("Epoch {epoch} batch {batch} {performance}".format(**log_info)), end="\r")

class LogisticRegression(nn.Module):
    def __init__(self, embed_dim, num_classes):
        super().__init__()
        self.fc = nn.Linear(embed_dim, num_classes)
        self.init_weights()

    def init_weights(self, init_range=5):
        self.fc.weight.data.uniform_(-init_range, init_range)
        self.fc.bias.data.zero_()

    def forward(self, embedded):
        return self.fc(embedded)

class MLP(nn.Module):
    def __init__(self, embed_dim, num_classes, dropout=0.25, n_hid=128):
        super().__init__()
        self.model = nn.Sequential(
            nn.Dropout(dropout),
            nn.Linear(embed_dim, n_hid),
            nn.ReLU(),
            nn.BatchNorm1d(n_hid),
            nn.Dropout(dropout),            
            nn.Linear(n_hid, n_hid // 4),
            nn.ReLU(),
            nn.BatchNorm1d(n_hid // 4),
            nn.Dropout(dropout),
            nn.Linear(n_hid // 4, num_classes),
        )
        self.init_weights()

    def init_weights(self):
        for m in self.model:
            if isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weight, a=0.01)
                nn.init.constant_(m.bias, 0)

    def forward(self, input_tensor):
        return self.model(input_tensor)

    def eval_per_layer(self, input_tensor):
        tensors = [input_tensor]
        current = input_tensor
        self.model.eval()
        for _layer in self.model:
            current = _layer(current)
            tensors.append(current)
        return tensors
