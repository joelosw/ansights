import yake
import spacy
from spacy import displacy
import os
import sys
sys.path.append('./')
print(sys.path)
if True:
    from src.utils.__RepoPath__ import repo_path


kw_extractor = yake.KeywordExtractor()
language = "de"
max_ngram_size = 1
deduplication_threshold = 0.9
numOfKeywords = 20
custom_kw_extractor = yake.KeywordExtractor(
    lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)


def extract_keyword_score(text, th=0.7):
    keywords = custom_kw_extractor.extract_keywords(text)
    keywords.sort(key=lambda x: x[1], reverse=False)
    return filter(lambda x: x[1] < th, keywords)
