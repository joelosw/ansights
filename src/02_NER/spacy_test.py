import spacy
from spacy import displacy
import os
import sys
sys.path.append('./')
print(sys.path)
if True:
    from src.utils.__RepoPath__ import repo_path
nlp = spacy.load("de_core_news_md")

with open(os.path.join(repo_path, 'data', 'arbeiter_aufruf_OCR_uncleaned.txt'), 'r') as f:
    text = f.read()
analyzed = nlp(text)
for word in analyzed.ents:
    print(word.text, word.label_)
for token in analyzed:
    if token.pos in [92, 96, 100]:
        pass
        print(
            f'| {token.text} \t | {token.pos_} \t | {token.pos} \t | {token.tag_}')

displacy.serve(analyzed)
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
