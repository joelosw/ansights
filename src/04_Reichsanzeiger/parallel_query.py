import asyncio
import aiohttp
import time
from threading import Lock
from fess_api import url_from_query_terms
from news_page import News_Page
import json
import sys
sys.path.append('./')
sys.path.append('./../')
sys.path.append('./../..')
if True:
    from src.utils.logger import get_logger
    from synonyms_iterator import synonyms_iterator_helper
logger = get_logger('ASYNC')


class NewsPageCollection():
    def __init__(self):
        self.collection = {}
        self.lock = Lock()

    def handle_entry(self, url: str, keywords: set):
        self.lock.acquire()
        try:
            self.collection[url] = News_Page(url, keywords)
        except KeyError:
            self.collection[url].add_keywords(keywords)
        self.lock.release()


def parallel_query(query_terms: list) -> dict:
    news_page_collection = NewsPageCollection()
    asyncio.run(main(query_terms, news_page_collection))
    logger.info(f'Parallel query finished with result: {news_page_collection.collection}')
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
        print("Unable to get url {} due to {}.".format(url, e.__class__))
    for result in result_json['response']['result']:
        current_url = result['url']
        news_page_collection.handle_entry(current_url, query_term)


async def main(query_terms, news_page_collection):
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*[query_reichsanzeiger_asnyc(query_term, session, news_page_collection) for query_term in query_terms])
    print("Finalized all. Return is a list of len {} outputs.".format(len(ret)))


if __name__ == '__main__':
    parallel_query(
        [('Streik, Arbeiter'), ('Arbeiter', 'Arbeitgeber'), ('Gasarbeiter', 'Streik')])
