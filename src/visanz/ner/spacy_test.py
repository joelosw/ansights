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
