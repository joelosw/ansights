import spacy
from spacy import displacy
import os
import sys
from enum import Enum

sys.path.append('./')
if True:
    from src.visanz.utils.__RepoPath__ import repo_path
nlp = spacy.load("de_core_news_md")


class WordType(Enum):
    PROP_NOUN = 96
    NOUN = 92
    VERB = 100


def extract_nouns_and_verbs(text):
    """
    The extract_nouns_and_verbs function accepts a string of text and returns a list of nouns and verbs.

    Parameters
    ----------
        text
            Pass in the text that is to be analyzed

    Returns
    -------
        A dictionary with keys that are wordtype objects and values that are lists of strings

    """

    analyzed = nlp(text)
    result = {WordType.NOUN: [], WordType.PROP_NOUN: [], WordType.VERB: []}
    for word in analyzed.ents:
        print(word.text, word.label_)
    for token in analyzed:
        if token.pos in [92, 96, 100]:
            result[WordType(token.pos)].append(token.text)
            print(
                f'| {token.text} \t | {token.pos_} \t | {token.pos} \t | {token.tag_}')
    #print(f'Result: {result}')
    return result


def extract_ner(text):
    """
    The extract_ner function accepts a string of text and returns a dictionary of named entities.
    The keys are the unique entity names, and the values are lists containing all occurrences 
    of each name in order.

    Parameters
    ----------
        text
            Pass in the text that we want to extract named entities from

    Returns
    -------

        A dictionary with the key being the word and value being the ner-label
    """

    analyzed = nlp(text)
    result = {}
    for word in analyzed.ents:
        result[word.text] = word.label_
    return result


if __name__ == '__main__':
    with open(os.path.join(repo_path, 'data', 'arbeiter_aufruf_OCR_uncleaned.txt'), 'r') as f:
        text = f.read()
    extract_nouns_and_verbs(text)
    # displacy.serve(analyzed)
# print("======= NOW ENGLISH==========")
# nlp_eng = spacy.load("en_core_web_trf")
# with open(os.path.join(repo_path, 'data', 'example_flyer_english.txt'), 'r') as f:
#     text_eng = f.read()
# analyzed_eng = nlp_eng(text_eng)
# for word in analyzed_eng.ents:
#     print(word.text, word.label_)
# for token in analyzed_eng:
#     print(token.text, token.pos_, token.dep_)
#displacy.serve(analyzed_eng, style="ent")
