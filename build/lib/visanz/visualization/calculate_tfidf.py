import os
import pandas as pd

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel

class TFIDF():

    def __init__(self, docs :list, verbose=False):
        self.docs = docs
        self.tf = self.get_tf(verbose=verbose)
        self.idf = self.get_idf(verbose=verbose)
        self.tf_idf = self.get_tf_idf(verbose=verbose)

    def get_tf(self, verbose=False):
        self.cv = CountVectorizer()
        self.word_count_vector = self.cv.fit_transform(self.docs)
        tf = pd.DataFrame(self.word_count_vector.toarray(), columns=self.cv.get_feature_names_out())
        if verbose:
            print('tf:', tf)
        return tf

    def get_idf(self, verbose=False):
        self.tfidf_transformer = TfidfTransformer()
        self.X = self.tfidf_transformer.fit_transform(self.word_count_vector)
        idf = pd.DataFrame({'feature_name':self.cv.get_feature_names_out(), 'idf_weights':self.tfidf_transformer.idf_})
        if verbose:
            print('idf:', idf)
        return idf

    def get_tf_idf(self, verbose=False):
        tf_idf = pd.DataFrame(self.X.toarray() ,columns=self.cv.get_feature_names_out())
        if verbose:
            print('tf_idf:', tf_idf)
        return tf_idf

    def get_cosine_similarity(self, comp_data, verbose=False):
        cosine_similarities = linear_kernel(self.tf_idf, comp_data)
        if verbose:
            print('Cosine Similarity:', self.cosine_similarities)
        
        return cosine_similarities


def get_reichsanzeiger_docs_relation_matrix(docs :list, keywords=None, verbose=False):

    docs_tfidf = TFIDF(docs, verbose=verbose)
    if keywords == None:
        cosine_similarities = docs_tfidf.get_cosine_similarity(comp_data=docs_tfidf.tf_idf, verbose=verbose)
    else:
        keywords_tfidf = TFIDF(keywords, verbose=verbose)
        cosine_similarities = docs_tfidf.get_cosine_similarity(comp_data=keywords_tfidf.tf_idf, verbose=verbose)

    return cosine_similarities

if __name__ == '__main__':

    example_docs = ['the cat see the mouse',    
                'the house has a tiny little mouse',
                'the mouse ran away from the house',
                'the cat finally ate the mouse',
                'the end of the mouse story'
               ]
    get_reichsanzeiger_docs_relation_matrix(docs=example_docs)