import os
import pandas as pd

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer


docs = ['the cat see the mouse',
      'the house has a tiny little mouse',
       'the mouse ran away from the house',
        'the cat finally ate the mouse',
       'the end of the mouse story'
       ]

class TFIDF():

    def __init__(self):
        self.cv = CountVectorizer()
        self.tf = 0
        self.idf = 0
        self.tf_idf = 0

    def set_tf(self):
        
        word_count_vector = self.cv.fit_transform(docs)
        self.tf = pd.DataFrame(word_count_vector.toarray(), columns=self.cv.get_feature_names())
        #print(tf)

    def set_idf(self):
        self.tfidf_transformer = TfidfTransformer()
        X = self.tfidf_transformer.fit_transform(word_count_vector)
        idf = pd.DataFrame({'feature_name':self.cv.get_feature_names(), 'idf_weights':tfidf_transformer.idf_})
        #print(idf)

    def set_tf_idf(self):
        self.tf_idf = pd.DataFrame(X.toarray() ,columns=cv.get_feature_names())
        print(tf_idf)
        return tf_idf

