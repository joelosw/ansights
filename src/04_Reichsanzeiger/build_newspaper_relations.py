from fess_api import query_and_process, count_for_query, query_reichsanzeiger
from itertools import combinations
import random
import logging
from tqdm import tqdm
fess_logger = logging.getLogger('FESS')
fess_logger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s : %(name)s : %(levelname)s : %(message)s', "%H:%M:%S")
console.setFormatter(formatter)
fess_logger.addHandler(console)


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

# First step, binary search at how many keywords we get results (presumably none if we throw in all keywords, and too many if we throw in 1 kw)


def binary_search_number_of_keywords(all_keywords: list, lowest=1, highest=None, highest_found=None):
    if highest is None:
        highest = len(all_keywords)
    fess_logger.debug(
        f'Lowest: {lowest}, highest: {highest}, highest_found: {highest_found}')
    if highest >= lowest:
        mid = (highest+lowest) // 2
        fess_logger.debug(f'Binary search trying to look for {mid} keywords')
        mid_count = count_for_query(random.sample(all_keywords, mid))
        fess_logger.debug(f'Found {mid_count} articles for {mid} keywords')
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
    fess_logger.info(f'Trying out {combs_length} combinations')

    for query_sample in tqdm(combinations(all_keywords, number_with_results), total=combs_length):
        result_json = query_reichsanzeiger(query_sample)['response']
        fess_logger.debug(
            f'Found {result_json["record_count"]} for {query_sample}')
        for result in result_json['result']:
            current_url = result['url']
            if current_url not in news_page.keys():
                news_page[current_url] = News_Page(current_url, query_sample)
            else:
                news_page[current_url].add_keywords(query_sample)
    fess_logger.debug(f'Created dict for {len(news_page)} scanned pages')
    return news_page


if __name__ == '__main__':
    example_query = "Spartakus Stuttgart 1919 streik gasarbeiter blibla blup das ist mir so egal ich teste nur die Suche".split(
        " ")
    print(binary_search_number_of_keywords(example_query))
    print(build_relations(example_query))
