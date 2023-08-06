import os
import re
import spacy
import wrappy
from hover.utils.common_nn import MLP

dir_path = os.path.dirname(__file__)

def get_text_to_vec():
    """
    :returns: a text vectorizer.
    """
    
    nlp = spacy.load('en_core_web_md')
    
    @wrappy.memoize(cache_limit=50000, persist_path=os.path.join(dir_path, 'text_to_vec.pkl'))
    def text_to_vec(text):
        """
        A more serious example of a text vectorizer.
        """
        clean_text = re.sub(r'[\t\n]', r' ', text)
        return nlp(clean_text, disable=nlp.pipe_names).vector
    
    return text_to_vec

def get_architecture():
    return MLP

def get_state_dict_path():
    return os.path.join(dir_path, 'model.pt')
