import spacy
from spacy import displacy
import os
import sys
sys.path.append('./')
print(sys.path)
if True:
    from src.utils.__RepoPath__ import repo_path
nlp = spacy.load("de_core_news_md")

with open(os.path.join(repo_path, 'src', '02_NER', 'example_flyer.txt'), 'r') as f:
    text = f.read()
analyzed = nlp(text)
for word in analyzed.ents:
    print(word.text, word.label_)
displacy.serve(analyzed, style='ent', )
