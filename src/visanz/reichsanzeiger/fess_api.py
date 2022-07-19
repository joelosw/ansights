import requests
from typing import Text, Union, Iterable, Dict, Any, Type, List
from datetime import datetime
import html2text
import sys
import numpy as np
sys.path.append('./')
sys.path.append('./../')
sys.path.append('./../..')
if True:
    from src.visanz.utils.logger import get_logger
fess_logger = get_logger('FESS')
JSON = Union[Dict[str, Any], List[Any], int, str, float, bool, Type[None]]
base_url = 'https://digi.bib.uni-mannheim.de/fess/json/?q='
tesseract5_label = '&fields.label=20211201'


example_query = "Spartakus Stuttgart 1919"


def query_reichsanzeiger(query_terms: Union[str, Iterable[str]]):
    """
    The query_reichsanzeiger function takes a query term or list of query terms 
    and returns the results from the FESS-API of the digitalized Reichhsanzeiger.
    Parameters
    ----------
        query_terms:Union[str, Iterable[str]]
            Allow the function to accept either a single string or an iterable of strings as input

    Returns
    -------
        A json response of the FESS-API

    """
    # If query_terms is of type list:
    fess_logger.debug(f'Will try to call fess-API for query: {query_terms}')
    url = url_from_query_terms(query_terms)
    fess_logger.debug(f'Calling {url}')
    response = requests.get(url)
    return response.json()


def url_from_query_terms(query_terms: Union[str, Iterable[str]]):
    """
    The url_from_query_terms function takes a string or list of strings and returns the urls for the query.
    The function first checks if the input is a list, tuple, or numpy array. If so it joins them with '+' to make one string.
    Then it replaces all spaces in that string with '+'. Finally it concatenates this new string to base.

    Parameters
    ----------
        query_terms:Union[str, Iterable[str]]
            Allow the function to handle a list of strings

    Returns
    -------
        The urls that are built from the query terms

    """
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
    """
    The add_date_to_results function adds a date key to the results dictionary.

    Parameters
    ----------
        results:Iterable[JSON]

    Returns
    -------
        result object with added date

    """
    for result in results:
        date = datetime.strptime(
            result['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ').date()
        result['date'] = date
    return results


def add_text_to_results(results: Iterable[JSON]) -> Iterable[JSON]:
    """
    The add_text_to_results function takes in a list of results and 
    adds the text from each NewsPage to its dictionary.

    Parameters
    ----------
        results:Iterable[JSON]

    Returns
    -------
        A list of dictionaries, each dictionary containing the new 'text' key

    """

    for result in results:
        data = requests.get(result['url_link'])
        text = html2text.html2text(data.text)
        result['text'] = text
    return results


def remove_unuseful_fields(results: Iterable[JSON]) -> Iterable[JSON]:
    """
    The remove_unuseful_fields function removes fields from the results that are not useful for our purposes.
    For example, we do not need to know what filetype a result is, or its title. We also do not need to know the host of a result
    or its filename. This function removes these unneeded fields.

    Parameters
    ----------
        results:Iterable[JSON]
            Iterate over the results of a query

    Returns
    -------

        A generator that yields the values of the json documents in results

    """
    for result in results:
        for key in ['filetype', 'title', 'content_title', 'digest', 'host', 'last_modified', 'content_length', 'created',
                    'site_path', 'doc_id', 'url', 'content_description', 'site', 'filename', 'boost', 'mimetype', '_id']:
            result.pop(key, None)
    return results


def query_and_process(query_term: str, add_text: bool = False):
    """
    The query_and_process function takes a query term as input and returns the results of the queries

    Parameters
    ----------
        query_term:str
            Specify the search term
        add_text:bool=False
            Add the text to the results

    Returns
    -------

        A list of dictionaries
    """
    result_json = query_reichsanzeiger(query_term)['response']
    results = result_json['result']
    results = add_date_to_results(remove_unuseful_fields(results))
    if add_text:
        results = add_text_to_results(results)
    return results


def count_for_query(query_term: str):
    """
    The count_for_query function takes a query term as input and returns the number of hits for that query.

    Parameters
    ----------
        query_term:str
            Define the query term that is used in the search

    Returns
    -------

        The number of hits for the query term

    Doc Author
    ----------
        Trelent
    """
    result_json = query_reichsanzeiger(query_term)['response']
    fess_logger.debug(f'Keys in result: {result_json.keys()}')
    return result_json['record_count']


def urls_from_query(query_term: str):
    """
    The urls_from_query function accepts a query term as input and returns a list of urls
    for the search results from the reichsanzeiger website

    Parameters
    ----------
        query_term:str
            Specify the search term

    Returns
    -------

        A list of urls for the given query term
    """
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
