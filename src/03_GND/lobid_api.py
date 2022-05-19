# Imports
import requests
import pandas as pd


def get_gnd_json(query: str, lobid_server='https://lobid.org/', catalog='gnd/search', 
                 filter='+(type:SubjectHeading)', verbose=False):
    """
        The get_gnd_json function accepts a query, URL components and filters as arguments and 
        returns the json file of the data item at a particular URL.

        :param query:str: Used to pass the keywords of our search.
        :param lobid_server='https://lobid.org/': Used to pass the base url of the page that is being scraped.
        :param catalog='gnd/search': Used to pass the catalog of the page that is being scraped.
        :param filter='+(type:SubjectHeading)': Used to add filters to our search.
        :param verbose=False: Used to print out relevant information for debugging.
        :return: A json.
    """

    base_url = lobid_server + catalog
    params = {'q': query,
              'filter': filter,
              'format': 'json'
              }

    r = requests.get(base_url, params=params)
    json_query=r.json()

    if verbose:
        print(json_query['id'])
        print('JSON File created')
    
    return json_query


def get_gnd_keywordRelations(keywords :list, max_items=10, print_output=True, verbose=True, 
                             remove_double=True, json_keys=['relatedTerm', 'gndSubjectCategory', 
                                                            'relatedPlaceOrGeographicName',
                                                            'preferredName','broaderTermInstantial',
                                                            'broaderTermGeneral', 'variantName']):
    
    """
        The get_gnd_keywordRelations function accepts keywords and keys as arguments and 
        returns the corrresponding output of the gnd for each keyword given a particular key in 
        a pandas dataframe.

        :param keywords :list: Used to pass the keywords of our search in list.
        :param json_keys==['relatedTerm', 'gndSubjectCategory', 'relatedPlaceOrGeographicName',
                           'preferredName','broaderTermInstantial', 'broaderTermGeneral', 
                           'variantName']: Used to pass the keys to scrape for linked terms.
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
                            stripped_term=term.strip(' ')
                            df[keyword][0][json_key].append(stripped_term)

                            if verbose:
                                print(f'Related Term for keyword "{keyword}" is {stripped_term}')

                except:
                    
                    # If value of key is a list or string! No explicit label key
                    try:
                        
                        for term in member[json_key].split(','):
                            stripped_term=term.strip(' ')
                            df[keyword][0][json_key].append(stripped_term)

                            if verbose:
                                print(f'Related Term for keyword "{keyword}" is {stripped_term}')

                    except:

                        try:

                            for term in member[json_key]:
                                df[keyword][0][json_key].append(term)

                                if verbose:
                                    print(f'Related Term for keyword "{keyword}" is {term}')

                        except:

                            if verbose:
                                print(f'Member {item+1} of kewyowrd "{keyword}" has no {json_key}.')
        
                if remove_double:
                    df[keyword][0][json_key]=list(dict.fromkeys(df[keyword][0][json_key]))


        if print_output:
            print()
            print(f'---------- GND OUTPUT: {keyword}  ----------')
            print(df[keyword][0])

    return df


# TEST
keys=['Goethe']
df=get_gnd_keywordRelations(keywords=keys, max_items=10, print_output=True, verbose=False, remove_double=True)
