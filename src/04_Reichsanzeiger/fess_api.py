import requests
from typing import Union, Iterable

base_url = 'https://digi.bib.uni-mannheim.de/fess/json/?q='
tesseract5_label = '&fields.label=20211201'


example_query = "Spartakus Stuttgart 1919"


def query_reichsanzeiger(query_terms: Union[str, Iterable[str]]):
    query_terms = query_terms.replace(' ', '+')
    print(f'Calling {base_url + query_terms + tesseract5_label}')
    response = requests.get(base_url + query_terms + tesseract5_label)
    return response.json()


result_json = query_reichsanzeiger(example_query)['response']
print(
    f'Got {result_json["record_count"]} results for query: {result_json["search_query"]}')
print(result_json['result'][0])
