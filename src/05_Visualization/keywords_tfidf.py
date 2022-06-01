import os
import pandas as pd

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

class KeyWords():

    def __init__(self, docs :list, verbose=False):
        self.docs = docs
        self.tf = self.get_tf(verbose=verbose)
        self.idf = self.get_idf(verbose=verbose)
        self.tf_idf = self.get_tf_idf(verbose=verbose)

    def get_tf(self, verbose=False):
        self.cv = CountVectorizer()
        self.word_count_vector = self.cv.fit_transform(self.docs)
        tf = pd.DataFrame(self.word_count_vector.toarray(), columns=self.cv.get_feature_names_out())
        tf.to_csv("x")
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

    def get_keywords(self, docs :list, topN=3):
        col_names = self.tf_idf.columns
        vals = self.tf_idf.values
        df = pd.DataFrame()
        for i in range(len(vals)):
            candidate_words = []
            for j in range(len(vals[i])):
                if vals[i][j] > 0:
                    candidate_words.append([col_names[j], float(vals[i][j])])
            candidate_words_df = pd.DataFrame(data=candidate_words, columns=['keywords', 'tf-idf'])
            keywords_df = candidate_words_df.sort_values(by='tf-idf', ascending=False).head(topN)
            df.loc[i, "title"] = str(i)
            df.loc[i, "content"] = docs[i]
            df.loc[i, "url"] = str(i)
            df.loc[i, "keywords"] = ' '.join(keywords_df["keywords"])
        return df

if __name__ == '__main__':

    example_docs = ['the cat see the mouse',
                'the house has a tiny little mouse',
                'the mouse ran away from the house',
                'the cat finally ate the mouse',
                'the end of the mouse story'
               ]
    kw = KeyWords(docs=example_docs)
    df = kw.get_keywords(example_docs)
    print(df)

