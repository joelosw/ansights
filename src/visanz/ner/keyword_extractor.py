
import yake
import spacy
from spacy import displacy
import os
import sys
sys.path.append('./')
print(sys.path)
if True:
    from src.visanz.utils.__RepoPath__ import repo_path


kw_extractor = yake.KeywordExtractor()
language = "de"
max_ngram_size = 1
deduplication_threshold = 0.9
numOfKeywords = 20
custom_kw_extractor = yake.KeywordExtractor(
    lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)


def extract_keyword_score(text: str, th: float = 0.7):
    """
    The extract_keyword_score function accepts a string of text and returns a list of keywords along with their scores.
    Only keywords with a score<th are returned. 
    (Lower score means more important)  

    Parameters
    ----------
        text:str
            Pass in the text that you want to extract keywords from
        th:float=0.7
            Set the threshold for the keywords

    Returns
    -------

        A list of tuples, where each tuple contains a keyword and its score

    Doc Author
    ----------
        Trelent
    """
    keywords = custom_kw_extractor.extract_keywords(text)
    print("===== Keyword scores: {keywords}")
    keywords.sort(key=lambda x: x[1], reverse=False)
    return filter(lambda x: x[1] < th, keywords)
