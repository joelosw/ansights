# incoming list with keywords with entitys

# return dictionary with keywords as keys and values with related subclass, subcategory, etc. 

# Example Arbeiter FILTER SCHLAGWORTE UND DEUTSCHLAND

import requests
import pandas as pd


def get_gnd_json(query: str, sru_server='https://lobid.org/', catalog='gnd/search', 
                 filter='+(type:SubjectHeading)', verbose=False):
    """
        The get_gnd_json function accepts a query, URL components and filters as arguments and 
        returns the json file of the data item at a particular URL.

        :param query:str: Used to pass the keywords of our search.
        :param sru_server='https://lobid.org/': Used to pass the base url of the page that is being scraped.
        :param catalog='gnd/search': Used to pass the catalog of the page that is being scraped.
        :param filter='+(type:SubjectHeading)': Used to add filters to our search.
        :param verbose=False: Used to print out relevant information for debugging.
        :return: A json.
    """

    base_url = sru_server + catalog
    params = {'q': query,
              'filter': filter,
              'format': 'json'
              }

    r = requests.get(base_url, params=params)
    json_query=r.json()

    if verbose:
        print('JSON File created')
    
    return json_query


def get_gnd_keywordRelations(keywords :list, json_keys=['relatedTerm', 'gndSubjectCategory'], 
                             max_items=10, print_output=True, verbose=True):
    
    """
        The get_gnd_keywordRelations function accepts keywords and keys as arguments and 
        returns the corrresponding output of the gnd for each keyword given a particular key in 
        a pandas dataframe.

        :param keywords :list: Used to pass the keywords of our search.
        :param json_keys=['relatedTerm', 'gndSubjectCategory']: Used to pass the keys to scrape for linked terms.
        :param max_items=10: Used to pass maximal number of items for each key.
        :param print_output=True: Used to print the dataframe for each keyword.
        :param verbose=False: Used to print out relevant information for debugging.
        :return: A pandas DataFrame.
    """

    df=pd.DataFrame()
    
    for keyword in keywords:
        json_query = get_gnd_json(query=keyword)
        
        try:
            total_items=json_query['totalItems']
        except:
            print(f'No items for keyword "{keyword}".')
            continue

        n_items = min(total_items, max_items)
        df[keyword] = [{json_key: list() for json_key in json_keys}]

        for item in range(n_items):
            
            member=json_query['member'][item]

            # get related Terms
            for json_key in json_keys:

                try:
                    for element in member[json_key]:
                        related_terms = element['label']
                        
                        for term in related_terms.split(','):
                            df[keyword][0][json_key].append(term.strip(' '))

                            if verbose:
                                stripped_term=term.strip(' ')
                                print(f'Related Term for keyword "{keyword}" is {stripped_term}')

                except:
                    if verbose:
                        print(f'Member {item+1} of kewyowrd "{keyword}" has no {json_key}.')

        if print_output:
            print()
            print(f'---------- GND OUTPUT: {keyword}  ----------')
            print(df[keyword][0])

    return df



keys=['Streik', 'Joel']
df=get_gnd_keywordRelations(keywords=keys, json_keys=['relatedTerm', 'gndSubjectCategory'], print_output=True, verbose=False)
