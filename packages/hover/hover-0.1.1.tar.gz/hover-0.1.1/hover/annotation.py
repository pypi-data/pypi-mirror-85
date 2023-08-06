"""
Submodule that handles the annotation interface, which is Prodigy in this case.
Data structure for communication: list of dictionaries.
"""
from abc import ABC, abstractmethod
from wrappy import todo
from hover.module_params import default_logger, PRODIGY_KEY_TRANSFORM_PREFIX
from rich.console import Console
from collections import OrderedDict
import time

logger = default_logger()

class AnnotationHistory:
    '''
    A stack of dicts which pretty-prints its most recent k elements.
    '''
    def __init__(self, columns, kwargs_mapping={}):
        from rich.table import Table
        self.console = Console()
        self.stack = []
        self.columns = [*columns, 'ANNOTATION', 'ACTION']
        
        def fresh_table():
            table = Table(show_header=True, header_style='bold magenta')
            for _col in self.columns:
                table.add_column(_col, **kwargs_mapping.get(_col, dict()))
            return table
        self.table_generator = fresh_table
        
    def add(self, data_dict):
        '''
        Add a schema-compliant element to the stack.
        '''
        args = tuple(data_dict.get(_col, '') for _col in self.columns)
        self.stack.append(args)
        
    def pop(self):
        '''
        Pop the last element.
        '''
        return self.stack.pop()
    
    def show(self, k, ascending=True):
        '''
        Display the last k elements in a table.
        '''
        table = self.table_generator()
        k = min(k, len(self.stack))
        if ascending:
            range_to_show = range(-k, 0, 1)
        else:
            range_to_show = range(-1, -k-1, -1)
        for _idx in range_to_show:
            _args = self.stack[_idx]
            table.add_row(*_args)
        self.console.print(table)

class BasePromptCollector(ABC):
    '''
    Base class of interactive user input collectors that only consider hashable unique prompts.
    '''
    def __init__(self,
                 collected,
                 key_func=lambda x: x,
                 value_func=lambda y: y,
                 display_func=lambda z: z,
                ):
        assert isinstance(collected, dict)
        for _func in [key_func, value_func, display_func]:
            assert callable(_func)
            
        self.collected = OrderedDict(collected)
        self.key_func = key_func
        self.value_func = value_func
        self.display_func = display_func
        self.console = Console()
        
    @abstractmethod
    def message(self, data_dict):
        '''
        Left as an abstract method to support custom prompt messages.
        '''
        pass
    
    def lookup(self, data_dict):
        '''
        Look up from the collected.
        '''
        key = self.key_func(data_dict)
        return self.collected.get(key, None)
    
    def collect(self, data_dict_list, **kwargs):
        '''
        Manages self.prompt() calls on a high level.
        '''
        for _data_dict in data_dict_list:
            _flag = self.prompt(_data_dict, **kwargs)
            
            if _flag:
                pass
            else:
                break
                
    def prompt(self, data_dict, history=None, interval=0.1):
        '''
        This functions is intended for running in Jupyter.
        Prompt the user for input, then return a boolean indicating whether to move on to the next prompt.
        '''
        from IPython.display import clear_output
        time.sleep(interval)
        clear_output(wait=True)
        
        if history:
            assert isinstance(history, AnnotationHistory)
            history.show(5)
            
        key = self.key_func(data_dict)
        
        if key in self.collected:
            if history:
                history.add({'ACTION': '[blue]READ[/blue]', **data_dict})
            return True
        
        self.message(data_dict)
        raw_value = input()
        flag = self.register(key, raw_value, history=history)
        return flag
    
    @abstractmethod
    def register(self, key, value, history=None):
        '''
        Left as an abstract method so that custom operations, such as undo and skip, can be supported.
        '''
        pass
    
class PromptCollector(BasePromptCollector):
    '''
    The vanilla prompt collector implementation.
    Uses a stack to implement an 'undo' operation.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompted = []
        
    def prompt(self, data_dict, **kwargs):
        '''
        Builds on top of the parent method.
        Updates the stack.
        '''
        self.prompted.append(data_dict)
        return super().prompt(data_dict, **kwargs)
    
    def register(self, key, value, **kwargs):
        '''
        Post-process the entered raw value.
        '''
        history = kwargs.get('history', None)
        # the undo button
        if value == 'x':
            assert len(self.prompted) >= 2, "Not enough annotations to go back"
            # go back to the previous prompt
            data_dict = self.prompted.pop()
            prev_data_dict = self.prompted.pop()
            prev_key, prev_value = self.collected.popitem(last=True)
            
            if history:
                history.add({'ACTION': '[red]UNDO[/red]', 'ANNOTAION': 'N/A', **prev_data_dict})
            flag = self.prompt(prev_data_dict, **kwargs)
            # try the current prompt again
            if flag:
                flag = self.prompt(data_dict, **kwargs)
            return flag
        
        # the skip button
        elif value == ' ':
            if history:
                data_dict = self.prompted[-1]
                history.add({'ACTION': '[yellow]SKIP[/yellow]', 'ANNOTATION': 'N/A', **data_dict})
            return True
        
        # the quit button
        elif value == 'quit':
            return False
        
        else:
            postprocessed = self.value_func(value)
            self.collected[key] = postprocessed
            if history:
                data_dict = self.prompted[-1]
                history.add({'ACTION': '[green]NEW[/GREEN]', 'ANNOTATION': value, **data_dict})
            return True
        
    def message(self, data_dict):
        '''
        Guide the user to enter an annotation.
        '''
        from rich.markdown import Markdown
        message_piece = "`x` to undo, ` ` to skip, `quit` to quit"
        self.console.print(Markdown(message_piece))
        display_dict = self.display_func(data_dict)
        for _key, _value in display_dict.items():
            self.console.print(Markdown(f"* {_key}: {_value}"))
        
        
class ProdigySession(ABC):
    """
    Create a burner object for sending data to Prodigy and collecting them.
    This is the base class.
    """

    def __init__(self, dictl, dataset_name="tmp", text_key="text"):
        """
        Initialize the dataset and data dicts to be annotated.
        :param dictl: each dict holds one whole entry of data.
        :type dictl: list of dicts
        :param dataset_name: the name of the (usually) temporary dataset.
        :type dataset_name: str
        :param text_key: the key in each dict in dictl that maps to the text to be annotated.
        :type text_key: str
        """
        import prodigy
        self._prodigy_specifics()
        self.dataset_name = dataset_name
        self.text_key = text_key
        self.input = [
            prodigy.set_hashes(self.process_dict_for_prodigy(_d)) for _d in dictl
        ]

    def _prodigy_specifics(self):
        """
        Handles specific utility parameters for interaction with Prodigy.
        """
        # keys that Prodigy uses internally never has '___' as prefix, so use it to avoid collision
        self._key_transform_prefix = PRODIGY_KEY_TRANSFORM_PREFIX
        # Prodigy assumes a 'text' key
        self._prodigy_text_key = "text"
        # annotation will override 'label' and 'answer'
        self._prodigy_keep_output = ["label", "answer"]
        self._prodigy_occupied = self._prodigy_keep_output + [self._prodigy_text_key]

    def process_dict_for_prodigy(self, input_dict):
        """
        Pre-processing that ensures smooth compatibility with Prodigy's internal mechanism.
        Specifically, transforms dict keys that would collide with Prodigy.
        :param input_dict: the dictionary holding data to be annotated.
        :type input_dict: dict
        :returns: dict -- transformed dict that gets sent to Prodigy.
        """
        ret_dict = dict()
        for _key, _value in input_dict.items():
            if _key == self.text_key:
                ret_dict[self._prodigy_text_key] = _value
            elif _key in self._prodigy_occupied:
                raise ValueError(
                    f"The {_key} field is occupied by Prodigy. Please use a different name."
                )
            else:
                _transformed_key = f"{self._key_transform_prefix}{_key}"
                ret_dict[_transformed_key] = _value
        return ret_dict

    def process_dict_from_prodigy(self, output_dict):
        """
        Post-processing that collects annotation and restores keys from previous transformations.
        :param output_dict: the dictionary holding data that has been annotated.
        :type output_dict: dict
        :returns: dict -- transformed dict that gets collected back to the developer.
        """
        ret_dict = dict()
        for _key, _value in output_dict.items():
            # restore the text key back to the original
            if _key == self._prodigy_text_key:
                ret_dict[self.text_key] = _value
            # restore fields that are present in the input
            elif _key.startswith(self._key_transform_prefix):
                _transformed_key = _key.replace(self._key_transform_prefix, "", 1)
                ret_dict[_transformed_key] = _value
            elif _key in self._prodigy_keep_output:
                ret_dict[_key] = _value
        return ret_dict

    @abstractmethod
    def serve(self, temp_jsonl_path, drop=False):
        """
        Different tasks use different Prodigy 'recipes'; this is a subroutine called by child classes.
        :param temp_jsonl_path: name of a temporary file to be created for launching Prodigy.
        :type temp_jsonl_path: str
        :param drop: whether to drop the Prodigy dataset if it already exists.
        :type drop: bool
        """
        import json
        import prodigy

        # connect to Prodigy's database
        self.db = prodigy.components.db.connect()
        # drop the existing dataset if instructed
        if self.db.get_dataset(self.dataset_name) and drop:
            self.db.drop_dataset(self.dataset_name)
        # create a new dataset
        self.db.add_dataset(self.dataset_name)
        # create a temporary file holding the data for Prodigy to load
        with open(temp_jsonl_path, "w") as f:
            f.write(
                "\n".join([json.dumps(_d, ensure_ascii=False) for _d in self.input])
            )

    def collect(self, drop=False):
        """
        Collect results when done with annotation.
        :param drop: whether to drop the dataset used in the session.
        :type drop: bool
        :returns: list of dict -- finalized entries of annotated data.
        """
        self.output = self.db.get_dataset(self.dataset_name)
        if drop:
            self.db.drop_dataset(self.dataset_name)
        return [self.process_dict_from_prodigy(_d) for _d in self.output]


class CustomTextcatSession(ProdigySession):
    """
    Prodigy session specifically for active-learning-based text classification.
    """

    def __init__(self, dictl, dataset_name="tmp", text_key="text"):
        super().__init__(dictl, dataset_name, text_key)

    def serve(
        self, model_module_name, labels, temp_jsonl_path=".dummy.jsonl", drop=False,
    ):
        """
        Launch a transfer learning textcat session.
        :param model_module_name: path to a local Python module in the working directory whose __init__.py file contains a text_to_vec() callable, architecture() callable, and a state_dict_path() callable.
        :type model_module_name: str
        :param labels: the classification labels that possibly apply.
        :type labels: list of str
        :param temp_jsonl_path: name of a temporary file to be created for launching Prodigy.
        :type temp_jsonl_path: str
        :param drop: whether to drop the Prodigy dataset if it already exists.
        :type drop: bool
        """
        import prodigy
        super().serve(temp_jsonl_path=temp_jsonl_path, drop=drop)
        args = [
            self.dataset_name,
            temp_jsonl_path,
            model_module_name,
            labels,
        ]
        prodigy.serve("textcat.text_vector_net", *args)


class LabelingFunctionSession(ProdigySession):
    """
    For manual accept/reject of labeling functions based on their logic and parameters.
    """

    def __init__(self, lf_candidates, dataset_name="tmp"):
        """
        Prepare an uuid mechanism to retrieve labeling functions after annotation.
        """
        import json

        self.uuid_to_lf = {str(_lf.uuid): _lf for _lf in lf_candidates}
        dictl = [{"bio": json.dumps(_lf.bio) if hasattr(_lf, 'bio') else "hand-crafted", "uuid": str(_lf.uuid)} for _lf in lf_candidates]
        super().__init__(dictl, dataset_name, "bio")

    def serve(
        self, temp_jsonl_path=".dummy.jsonl", drop=False,
    ):
        """
        Launch a Accept/Reject session for labeling functions without a model in the loop.
        :param temp_jsonl_path: name of a temporary file to be created for launching Prodigy.
        :type temp_jsonl_path: str
        :param drop: whether to drop the Prodigy dataset if it already exists.
        :type drop: bool
        """
        import prodigy
        super().serve(temp_jsonl_path=temp_jsonl_path, drop=drop)
        prodigy.serve(
            "lf.accept_reject", self.dataset_name, temp_jsonl_path,
        )

    def collect(self):
        """
        Collect labeling functions that are accepted.
        """
        dictl = super().collect(drop=True)
        return [self.uuid_to_lf[_d["uuid"]] for _d in dictl if _d["answer"] == "accept"]


class BokehVisualizedSession(object):
    """
    Just a conjecture as this stage.
    The idea is to annotate labeling functions, and to embed a bokeh plot alongside each labeling function.
    For now, a separate Bokeh plot will suffice.. but who knows, this can be desirable in the future.
    """

    @todo("Not implemented")
    def __init__(self):
        pass
