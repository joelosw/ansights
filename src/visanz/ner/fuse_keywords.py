# requires python>3.9
import os
from spacy_test import extract_nouns_and_verbs, WordType
from keyword_extractor import extract_keyword_score
import logging
import sys
sys.path.append('./')
if True:
    from src.visanz.utils.__RepoPath__ import repo_path
    from src.visanz.utils.logger import get_logger


ner_logger = get_logger('NER')


def fuse(text: str, max_nouns: int = None, max_verbs: int = None):
    """
    The fuse function takes a string and returns a dictionary of the top
    nouns, verbs, and proper nouns in that text. The number of each to return
    is optional; if not specified, all are returned.

    Parameters
    ----------
        text:str
            Pass the text that should be processed
        max_nouns:int=None
            Specify the maximum number of nouns to be returned
        max_verbs:int=None
            Specify how many verbs to return

    Returns
    -------
        A dictionary with the words and their scores
    """
    scores = dict(extract_keyword_score(text))
    ner_logger.debug(f' Scores: {scores}')
    types = extract_nouns_and_verbs(text)
    words_with_scores = {}
    prop_nouns = []
    for noun in types[WordType.PROP_NOUN]:
        try:
            prop_nouns.append((noun, scores[noun]))
        except KeyError as e:
            print(e)
            ner_logger.warning(f'Could not get score for "{noun}"')

    nouns = []
    for noun in types[WordType.NOUN]:
        try:
            nouns.append((noun, scores[noun]))
        except KeyError as e:
            print(e)
            ner_logger.warning(f'Could not get score for "{noun}"')

    verbs = []
    for verb in types[WordType.VERB]:
        try:
            verbs.append((verb, scores[verb]))
        except KeyError as e:
            print(e)
            ner_logger.warning(f'Could not get score for "{verb}"')

    if max_nouns:
        prop_nouns.sort(key=lambda x: x[1], reverse=False)
        num_prop = len(prop_nouns)
        nouns.sort(key=lambda x: x[1], reverse=False)
        num_nouns = len(nouns)
        candidates = []
        for i in range(max_nouns):
            if num_prop > i:
                candidates.append(prop_nouns[i])
            elif num_nouns > i - num_prop:
                candidates.append(nouns[i - num_prop])
            else:
                ner_logger.warning(
                    f'Could only get {num_prop + num_nouns} nouns of the wanted {max_nouns}')
        words_with_scores = {**words_with_scores, **dict(candidates)}
    else:
        words_with_scores = {**words_with_scores,
                             **dict(prop_nouns), **dict(nouns)}

    if max_verbs:
        verbs.sort(key=lambda x: x[1], reverse=False)
        num_verbs = len(verbs)
        candidates = []
        for i in range(max_verbs):
            if num_verbs > i:
                candidates.append(verbs[i])
            else:
                ner_logger.warning(
                    f'Could only get {num_verbs} verbs of the wanted {max_verbs}')
        words_with_scores = {**words_with_scores, **dict(candidates)}
    else:
        words_with_scores = {**words_with_scores, **dict(verbs)}
    return words_with_scores


if __name__ == '__main__':
    with open(os.path.join(repo_path, 'data', 'arbeiter_aufruf_OCR_uncleaned.txt'), 'r') as f:
        text = f.read()
    print(fuse(text, max_nouns=4, max_verbs=2))
