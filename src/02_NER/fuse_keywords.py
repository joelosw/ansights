import os
from spacy_test import extract_nouns_and_verbs
from keyword_extractor import extract_keyword_score, WordType
import logging
import sys
sys.path.append('./')
print(sys.path)
if True:
    from src.utils.__RepoPath__ import repo_path


ner_logger = logging.getLogger('FESS')
ner_logger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s : %(name)s : %(levelname)s : %(message)s', "%H:%M:%S")
console.setFormatter(formatter)
ner_logger.addHandler(console)


def fuse(text: str, max_nouns: int = None, max_verbs: int = None):
    scores = dict(extract_keyword_score(text))
    types = extract_nouns_and_verbs(text)
    words_with_scores = {}
    prop_nouns = {}
    for noun in types[WordType.PROP_NOUN]:
        try:
            prop_nouns[noun] = scores[noun]
        except:
            ner_logger.warning(f'Could not get score for "{noun}"')

    nouns = {}
    for noun in types[WordType.NOUN]:
        try:
            nouns[noun] = scores[noun]
        except:
            ner_logger.warning(f'Could not get score for "{noun}"')

    verbs = {}
    for verb in types[WordType.VERB]:
        try:
            verbs[verb] = scores[verb]
        except:
            ner_logger.warning(f'Could not get score for "{verb}"')

    if max_nouns is not None:
        pass
        # TODO: Implement...
    else:
        words_with_scores = words_with_scores | prop_nouns | nouns


if __name__ == '__main__':
    with open(os.path.join(repo_path, 'data', 'arbeiter_aufruf_OCR_uncleaned.txt'), 'r') as f:
        text = f.read()
