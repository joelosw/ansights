import os
import pandas as pd

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import linear_kernel

class TFIDF():

    def __init__(self, docs :list):
        self.docs = docs
        self.tf = 0
        self.idf = 0
        self.tf_idf = 0
        self.cosine_similarities = []

    def set_tf(self, verbose=False):
        self.cv = CountVectorizer()
        self.word_count_vector = self.cv.fit_transform(self.docs)
        self.tf = pd.DataFrame(self.word_count_vector.toarray(), columns=self.cv.get_feature_names_out())
        if verbose:
            print('tf:', self.tf)

    def set_idf(self, verbose=False):
        self.tfidf_transformer = TfidfTransformer()
        self.X = self.tfidf_transformer.fit_transform(self.word_count_vector)
        self.idf = pd.DataFrame({'feature_name':self.cv.get_feature_names_out(), 'idf_weights':self.tfidf_transformer.idf_})
        if verbose:
            print('idf:', self.idf)

    def set_tf_idf(self, verbose=False):
        self.tf_idf = pd.DataFrame(self.X.toarray() ,columns=self.cv.get_feature_names_out())
        if verbose:
            print('tf_idf:', self.tf_idf)

    def set_cosine_similarity(self, verbose=False):
        self.cosine_similarities = linear_kernel(self.tf_idf, self.tf_idf)
        if verbose:
            print('Cosine Similarity:', self.cosine_similarities)


def get_reichsanzeiger_docs_relation_matrix(docs :list, verbose=False):

    tfidf_object = TFIDF(docs)
    tfidf_object.set_tf(verbose=verbose)
    tfidf_object.set_idf(verbose=verbose)
    tfidf_object.set_tf_idf(verbose=verbose)
    tfidf_object.set_cosine_similarity(verbose=verbose)

    return tfidf_object.cosine_similarities

if __name__ == '__main__':

    example_docs = ['the cat see the mouse',    
                'the house has a tiny little mouse',
                'the mouse ran away from the house',
                'the cat finally ate the mouse',
                'the end of the mouse story'
               ]
    get_reichsanzeiger_docs_relation_matrix(docs=example_docs)