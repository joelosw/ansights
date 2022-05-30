from fess_api import query_and_process, count_for_query, query_reichsanzeiger
from itertools import combinations
import random
import logging
import sys
from tqdm import tqdm
sys.path.append('./')
sys.path.append('./../')
sys.path.append('./../..')
if True:
    from src.utils.logger import get_logger
logger = get_logger('REL')


class News_Page:
    keywords: set = set()
    url: str

    def __init__(self, url, init_keywords=None):
        self.url = url
        if isinstance(init_keywords, str):
            init_keywords = init_keywords.split(' ')
        else:
            init_keywords = init_keywords
        self.keywords.update(init_keywords)

    def add_keywords(self, additional_keywords):
        self.keywords.update(additional_keywords)

    def __eq__(self, other):
        other.url == self.url

    def common_keywords(self, other):
        return self.keywords.intersection(other.keywords)

    def __str__(self) -> str:
        return f'\n ========== \n Newspaper Page  from URL: \n {self.url} with keywords {self.keywords} ====== \n'

    def __repr__(self) -> str:
        return self.__str__()
# First step, binary search at how many keywords we get results (presumably none if we throw in all keywords, and too many if we throw in 1 kw)


def binary_search_number_of_keywords(all_keywords: list, lowest=1, highest=None, highest_found=None):
    if highest is None:
        highest = len(all_keywords)
    logger.debug(
        f'Lowest: {lowest}, highest: {highest}, highest_found: {highest_found}')
    if highest >= lowest:
        mid = (highest+lowest) // 2
        logger.debug(f'Binary search trying to look for {mid} keywords')
        mid_count = count_for_query(random.sample(all_keywords, mid))
        logger.debug(f'Found {mid_count} articles for {mid} keywords')
        if mid_count == 1:
            return mid
        elif mid_count == 0:
            if highest_found:
                # We found something before, but now we find 0 --> too many paramters
                return highest_found
            else:
                # We have not found any results yet -> search for fewer terms
                return binary_search_number_of_keywords(all_keywords, lowest=lowest, highest=mid-1)
        elif mid_count > 0:
            return binary_search_number_of_keywords(all_keywords, mid+1, highest, highest_found=mid)

    else:
        if highest_found:
            return highest_found
        else:
            raise Warning(
                'Could not find number of keywords suffiecient to query Reichsanzeigeer')


def build_relations(all_keywords: list):
    number_with_results = binary_search_number_of_keywords(all_keywords)
    news_page = dict()
    combs = combinations(all_keywords, number_with_results)
    combs_length = sum(1 for _ in combs)
    logger.info(f'Trying out {combs_length} combinations')

    for query_sample in tqdm(combinations(all_keywords, number_with_results), total=combs_length):
        result_json = query_reichsanzeiger(query_sample)['response']
        logger.debug(
            f'Found {result_json["record_count"]} for {query_sample}')
        for result in result_json['result']:
            current_url = result['url']
            if current_url not in news_page.keys():
                news_page[current_url] = News_Page(current_url, query_sample)
            else:
                news_page[current_url].add_keywords(query_sample)
    logger.debug(f'Created dict for {len(news_page)} scanned pages')
    return news_page


def get_main_words(keywords_dict):
    """
    Return main words from dictionary, without synonyms
    """
    return keywords_dict.keys()


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
            result[key] = [v for v in value if v is not None]
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


def build_relations_with_synonyms(keywords_dict: dict):
    # number_with_results = binary_search_number_of_keywords(
    #     get_main_words(keywords_dict))
    number_with_results = 3
    synonyms = synonyms_iterator_helper(keywords_dict, number_with_results)
    iterator = iter(synonyms)
    for n_gram in iterator:
        logger.debug(f' ====> Got new ngram: ({n_gram})')


if __name__ == '__main__':
    example_query = ['Arbeiter', 'Funktionen', 'Religionszugehörigkeit', 'Tätigkeiten', 'Einzelne Berufe'
                     'Arbeitgeber', 'Arbeitsgestaltung', 'Personalpolitik', 'Arbeit'
                     'Gasarbeiter', 'Betriebe', 'Unternehmen', 'Agrarpolitik'
                     'auszumachen', 'streiken']
    example_synonyms = {'Arbeiter': ['Einzelne Berufe', 'Tätigkeiten'], 'Arbeitgeber': [
        'Arbeit', 'Personalpolitik', 'Arbeitsgestaltung'], 'Betriebe': [], 'Gasarbeiter': []}
    # example_query = "Spartakus Stuttgart 1919 Karlsruhe".split(
    #     " ")
    # print(binary_search_number_of_keywords(example_query))
    # print(build_relations(example_query))
    build_relations_with_synonyms(example_synonyms)
