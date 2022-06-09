
import requests
from typing import Text, Union, Iterable, Dict, Any, Type, List
from datetime import datetime
import html2text
import sys
import numpy as np
sys.path.append('./')
sys.path.append('./../')
sys.path.append('./../..')

from src.visanz.utils.logger import get_logger

fess_logger = get_logger('FESS')
JSON = Union[Dict[str, Any], List[Any], int, str, float, bool, Type[None]]
base_url = 'https://digi.bib.uni-mannheim.de/fess/json/?q='
tesseract5_label = '&fields.label=20211201'


example_query = "Spartakus Stuttgart 1919"


def query_reichsanzeiger(query_terms: Union[str, Iterable[str]]):
    # If query_terms is of type list:
    fess_logger.debug(f'Will try to call fess-API for query: {query_terms}')
    url = url_from_query_terms(query_terms)
    fess_logger.debug(f'Calling {url}')
    response = requests.get(url)
    return response.json()


def url_from_query_terms(query_terms: Union[str, Iterable[str]]):
    if isinstance(query_terms, list) or isinstance(query_terms, tuple) or isinstance(query_terms, np.ndarray):
        query_terms = '+'.join(query_terms)
    elif isinstance(query_terms, str):
        query_terms = query_terms.replace(' ', '+')
    else:  # otherwise
        raise Exception(
            "Call can only handle list of keywords or string with space-seperated keywords")
    url = base_url + query_terms + tesseract5_label
    return url


def add_date_to_results(results: Iterable[JSON]) -> Iterable[JSON]:
    for result in results:
        date = datetime.strptime(
            result['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
        result['date'] = date
    return results


def add_text_to_results(results: Iterable[JSON]) -> Iterable[JSON]:
    for result in results:
        data = requests.get(result['url_link'])
        text = html2text.html2text(data.text)
        result['text'] = text
    return results


def remove_unuseful_fields(results: Iterable[JSON]) -> Iterable[JSON]:
    for result in results:
        for key in ['filetype', 'title', 'content_title', 'digest', 'host', 'last_modified', 'content_length', 'created',
                    'site_path', 'doc_id', 'url', 'content_description', 'site', 'filename', 'boost', 'mimetype', '_id']:
            result.pop(key, None)
    return results


def query_and_process(query_term: str, add_text: bool = False):
    result_json = query_reichsanzeiger(query_term)['response']
    results = result_json['result']
    results = add_date_to_results(remove_unuseful_fields(results))
    if add_text:
        results = add_text_to_results(results)
    return results


def count_for_query(query_term: str):
    result_json = query_reichsanzeiger(query_term)['response']
    fess_logger.debug(f'Keys in result: {result_json.keys()}')
    return result_json['record_count']


def urls_from_query(query_term: str):
    result_json = query_reichsanzeiger(query_term)['response']
    urls = []
    for result in result_json['result']:
        urls.append(result['url'])
    return urls


if __name__ == '__main__':
    result_json = query_reichsanzeiger(example_query)['response']
    print(
        f'Got {result_json["record_count"]} results for query: {result_json["search_query"]}')
    results = result_json['result']

    results = add_text_to_results(
        add_date_to_results(remove_unuseful_fields(results)))
