
import sys
import re
from itertools import combinations
sys.path.append('./')
sys.path.append('./../')
sys.path.append('./../..')
if True:
    from src.utils.logger import get_logger
logger = get_logger('REL')


class synonyms_iterator_helper():
    def __init__(self, keywords_dict: dict, n_gram: int):
        """
        :param self: Refer to the object of the class
        :param keywords_dict:dict: Initialize the keywords dictionary, which is used to store the keywords and their corresponding scores
        :param n_gram:int: Set the number of words in a phrase that will be used to search for the keywords
        :return: The object itself, which is the instance of the class
        """
        self.keywords = self.clean_dict(keywords_dict)
        self.n_gram = n_gram
        self.words_with_synonyms = self.words_with_synonyms()

    def clean_dict(self, keywords_dict) -> dict:
        result = {}
        for key, value in keywords_dict.items():
            result[key] = [re.sub(r'[^a-z A-Z]', '', v) for v in value if v is not None]
            if len(result[key]) > 0:
                # If we have synonyms for a word, also append the word itself, so that it is not skipped
                result[key].insert(0, key)
        return result

    def words_with_synonyms(self) -> list:
        result = []
        for key, value in self.keywords.items():
            if len(value) > 0:
                result.append(key)
        return result

    def get_keyword_list(self, syn_word: int, syn_k: int) -> list:
        result = list(self.keywords.keys())

        if syn_word >= len(self.words_with_synonyms):
            logger.warning(f'No synonym word found at index {syn_word}')
            return None
        syn_word = self.words_with_synonyms[syn_word]

        if syn_k >= len(self.keywords[syn_word]):
            logger.warning(
                f'Word {syn_word} has not synonym at index {syn_k}')
            return None
        result.remove(syn_word)
        syn = self.keywords[syn_word][syn_k]
        result.append(syn)
        return result

    def get_mother_word(self, synonym: str):
        """Get the main word  instead of synonym.
        Raise Error if not existing

        Parameters
        ----------
        synonym : str
            synonym to find the main word for
        """

        for k, v in self.keywords.items():
            if synonym == k:
                return k
            if synonym in v:
                return k

        raise ValueError(f"Synonym {synonym} not found in keyword dict")

    def get_multiple_motherwords(self, synonyms: list):
        result = []
        for synonym in synonyms:
            result.append(self.get_mother_word(synonym))
        return result

    def __iter__(self):
        self.n = 0
        self.syn_word_n = 0
        self.syn_k = 0
        keyword_list = self.get_keyword_list(self.syn_word_n, self.syn_k)
        logger.info(f'Setting Up Combinations iterator with: {keyword_list}')
        self.current_combination = combinations(
            keyword_list, self.n_gram)
        self.comb_iter = iter(self.current_combination)
        return self

    def __next__(self):

        if self.syn_word_n < len(self.words_with_synonyms):
            syn_word = self.words_with_synonyms[self.syn_word_n]
            synonyms = self.keywords[syn_word]
            logger.debug(f'Getting synonym for word {syn_word}: {synonyms}')
            if self.syn_k < len(synonyms):
                logger.debug(
                    f'Using {synonyms[self.syn_k]} instead of {syn_word}')
                try:
                    result = next(self.comb_iter)
                    return result
                except StopIteration:
                    self.syn_k += 1
                    if self.syn_k < len(synonyms):
                        logger.debug(
                            f'Using next synonym {synonyms[self.syn_k]} instead of {syn_word}')
                        keyword_list = self.get_keyword_list(
                            self.syn_word_n, self.syn_k)
                        logger.debug(
                            f'Setting Up Combinations iterator with: {keyword_list}')
                        self.current_combination = combinations(
                            keyword_list, self.n_gram)
                        self.comb_iter = iter(self.current_combination)
                        return next(self.comb_iter)
                    else:
                        logger.debug(
                            f'No More synonyms for {syn_word}, moving to next word')
                        # return self.__next__()

            else:
                self.syn_word_n += 1
                if self.syn_word_n < len(self.words_with_synonyms):
                    self.syn_k = 0
                    keyword_list = self.get_keyword_list(
                        self.syn_word_n, self.syn_k)
                    logger.debug(
                        f'Setting Up Combinations iterator with: {keyword_list}')
                    self.current_combination = combinations(
                        keyword_list, self.n_gram)
                    self.comb_iter = iter(self.current_combination)
                    return next(self.comb_iter)
                else:
                    raise StopIteration

        else:
            raise StopIteration
