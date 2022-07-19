from fess_api import query_and_process, count_for_query, query_reichsanzeiger
from news_page import News_Page
from parallel_query import parallel_query
from itertools import combinations, chain
import random
import logging
import sys
import html2text
import requests
from tqdm import tqdm
sys.path.append('./')
sys.path.append('./../')
sys.path.append('./../..')
if True:
    from src.visanz.utils.logger import get_logger
    from synonyms_iterator import synonyms_iterator_helper
logger = get_logger('REL')


# First step, binary search at how many keywords we get results (presumably none if we throw in all keywords, and too many if we throw in 1 kw)


def binary_search_number_of_keywords(all_keywords: list, lowest=1, highest=None, highest_found=None) -> int:
    """
    The function uses recursive binary search to find the optimal number of keywords, i.e., 
    it searches for the smallest possible number that still gives more than one result per keyword.

    Parameters
    ----------
        all_keywords:list
            Search for the number of keywords that gives a result with one article
        lowest=1
            Make sure the function doesn't return 0
        highest=None
            Make sure that the function will search for a number of keywords between lowest and highest
        highest_found=None
            Keep track of the highest value that has been found so far

    Returns
    -------

        The number of keywords that returns enough articles

    """

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


def build_relations_async(all_keywords: list, sample=None):
    """
    The build_relations_async function takes a list of keywords and returns a list with unique instances of NewsPage.
    This is done asynchronously with multiple threads

    Parameters
    ----------
        all_keywords:list
            Create the combinations of keywords that are used to query the news api
        sample=None
            Specify the number of combinations to be used

    Returns
    -------

        A list with NewsPages

    """
    number_with_results = binary_search_number_of_keywords(all_keywords)
    if sample is None:
        combs = list(combinations(all_keywords, number_with_results))
    else:
        main_iter = chain.from_iterable(combinations(
            all_keywords, num) for num in range(1, len(all_keywords)))
        powerset = list(main_iter)
        logger.debug(f'Going to sample {sample} from {len(powerset)}')
        combs = random.sample(powerset, min(sample, len(powerset)))
    logger.info(f'Trying out {len(combs)} combinations')
    news_page = parallel_query(combs)
    logger.debug(f'Created dict for {len(news_page)} scanned pages')
    return list(news_page.values())


def build_relations(all_keywords: list):
    """
    The build_relations_async function takes a list of keywords and returns a list with unique instances of NewsPage.

    Parameters
    ----------
        all_keywords:list
            Create the combinations of keywords that are used to query the news api
        sample=None
            Specify the number of combinations to be used

    Returns
    -------

        A list with NewsPages

    """
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
    return list(news_page.values())


def get_main_words(keywords_dict):
    """
    Return main words from dictionary, without synonyms
    """
    return keywords_dict.keys()


def build_relations_with_synonyms(keywords_dict: dict):
    """
    The build_relations_with_synonyms function takes a dictionary of keywords and synonyms as input.
    It then queries the reichsanzeiger search engine for each keyword and its synonyms,
    and stores the results in a News_Page object. The function returns a list with all News_Pages.

    Parameters
    ----------
        keywords_dict:dict
            Get the keywords to search for

    Returns
    -------

        A dictionary with the url as key and a news_page object as value
    """

    number_with_results = binary_search_number_of_keywords(
        get_main_words(keywords_dict))
    news_page = dict()
    synonyms = synonyms_iterator_helper(keywords_dict, number_with_results)
    synonyms_list = list(synonyms)
    logger.info(f'Mem-Size of all synonyms: {sys.getsizeof(synonyms_list)}')
    for query_sample in tqdm(synonyms_list):
        # logger.debug(f' ====> Got new ngram: ({query_sample})')
        if query_sample is None:
            logger.warning(
                f'Got empty query_sample from iterator. Continuing....')
            continue
        keyword_sample = synonyms.get_multiple_motherwords(query_sample)
        result_json = query_reichsanzeiger(query_sample)['response']
        logger.debug(
            f'Found {result_json["record_count"]} for {query_sample}')
        for result in result_json['result']:
            current_url = result['url']
            if current_url not in news_page.keys():
                news_page[current_url] = News_Page(current_url, keyword_sample)
            else:
                news_page[current_url].add_keywords(keyword_sample)
    logger.debug(f'Created dict for {len(news_page)} scanned pages')
    return list(news_page.values())


def build_relations_with_synonyms_async(keywords_dict: dict, num_workers: int = 10, sample: int = None):
    """
    The build_relations_with_synonyms function takes a dictionary of keywords and synonyms as input.
    It then queries the reichsanzeiger search engine for each keyword and its synonyms,
    and stores the results in a News_Page object. The function returns a list with all News_Pages.
    This is done asynchronously.

    Parameters
    ----------
        keywords_dict:dict
            Get the keywords to search for

    Returns
    -------
        A dictionary with the url as key and a news_page object as value
    """
    # number_with_results = binary_search_number_of_keywords(
    #     get_main_words(keywords_dict))
    number_with_results = 3
    synonyms = synonyms_iterator_helper(keywords_dict, number_with_results)
    if sample:
        main_iter = chain.from_iterable(iter(synonyms_iterator_helper(
            keywords_dict, num)) for num in range(1, len(keywords_dict)))
        # Get rid of Nones...
        powerset = [query for query in main_iter if query]
        logger.debug(f'Going to sample {sample} from {len(powerset)}')
        combs = random.sample(powerset, min(sample, len(powerset)))
    else:
        combs = list(synonyms)

    logger.info(f'Trying out {len(combs)} combinations')
    news_page = parallel_query(combs, num_workers, synonyms)
    logger.debug(f'Created dict for {len(news_page)} scanned pages')
    return list(news_page.values())


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
