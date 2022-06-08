import asyncio
import aiohttp
import numpy as np
from threading import Lock
from fess_api import url_from_query_terms
from news_page import News_Page
import sys
import time
sys.path.append('./')
sys.path.append('./../')
sys.path.append('./../..')
if True:
    from src.visanz.utils.logger import get_logger
    from synonyms_iterator import synonyms_iterator_helper
logger = get_logger('ASYNC')


class NewsPageCollection():
    def __init__(self, synonyms_iterator_helper: synonyms_iterator_helper = None):
        self.collection = {}
        self.lock = Lock()
        self.syn_helper = synonyms_iterator_helper

    def handle_entry(self, url: str, keywords: set):
        if self.syn_helper:
            keywords = self.syn_helper.get_multiple_motherwords(
                keywords)
        self.lock.acquire()
        try:
            self.collection[url] = News_Page(url, keywords)
        except KeyError:
            self.collection[url].add_keywords(keywords)
        self.lock.release()


def parallel_query(query_terms: list, num_workers: int = None, synonyms_helper: synonyms_iterator_helper = None) -> dict:
    news_page_collection = NewsPageCollection(synonyms_helper)
    if num_workers:
        asyncio.run(main_workers(
            query_terms, news_page_collection, num_workers))
    else:
        asyncio.run(main(query_terms, news_page_collection))
    logger.info(
        f'Parallel query finished with result: {news_page_collection.collection}')
    return news_page_collection.collection


async def query_reichsanzeiger_asnyc(query_term, session, news_page_collection):
    url = url_from_query_terms(query_term)
    logger.debug(f'Thread Quering: {url}')
    try:
        async with session.get(url=url) as response:
            result_json = await response.json()
            # result_json = await result.text()
            logger.debug(
                f'Thread {url} result: {result_json["response"].keys()}')
    except Exception as e:
        logger.debug(
            "Unable to get url {} due to {}.".format(url, e.__class__))
    for result in result_json['response']['result']:
        current_url = result['url']
        news_page_collection.handle_entry(current_url, query_term)


async def query_reichsanzeiger_worker(query_terms, session, news_page_collection):
    for query_term in query_terms:
        url = url_from_query_terms(query_term)
        logger.debug(f'Thread Quering: {url}')
        try:
            async with session.get(url=url) as response:
                result_json = await response.json()
                # result_json = await result.text()
                logger.debug(
                    f'Thread {url} result: {result_json["response"].keys()}')
        except Exception as e:
            logger.debug(
                "Unable to get url {} due to {}.".format(url, e.__class__))
        for result in result_json['response']['result']:
            current_url = result['url']
            news_page_collection.handle_entry(
                current_url, query_term)


async def main(query_terms, news_page_collection):
    async with aiohttp.ClientSession() as session:
        workers = [query_reichsanzeiger_asnyc(
            query_term, session, news_page_collection) for query_term in query_terms]
        ret = await asyncio.gather(*workers)
    logger.debug(
        "Finalized all. Return is a list of len {} outputs.".format(len(ret)))


async def main_workers(query_terms, news_page_collection, num_workers: int = 10):
    async with aiohttp.ClientSession() as session:
        workers = [query_reichsanzeiger_worker(
            worker_terms, session, news_page_collection) for worker_terms in np.array_split(list(query_terms), num_workers)]
        ret = await asyncio.gather(*workers)
        logger.debug(
            "Finalized all. Return is a list of len {} outputs.".format(len(ret)))

if __name__ == '__main__':
    t1 = time.time()
    result = parallel_query(
        [('Streik, Arbeiter'), ('Arbeiter', 'Arbeitgeber'),
         ('Gasarbeiter', 'Streik'), ('streik'), ('Arbeiter'),
         ('Gasarbeiter', 'Streik'), ('streik'), ('Arbeiter'),
         ('Gasarbeiter', 'Streik'), ('streik'), ('Arbeiter'),
         ('Gasarbeiter', 'Streik'), ('streik'), ('Arbeiter'),
         ('Gasarbeiter', 'Streik'), ('streik'), ('Arbeiter'),
         ('Gasarbeiter', 'Streik'), ('streik'), ('Arbeiter')],
        num_workers=None)
    logger.info('Query with result: {} took {} seconds.'.format(
        len(result), time.time()-t1))
