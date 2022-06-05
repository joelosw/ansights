# Imports
import requests
import pandas as pd
import spacy
import sys

from collections import defaultdict

sys.path.append('./')
if True:
    from src.utils.__RepoPath__ import repo_path
nlp = spacy.load("de_core_news_md")


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
    json_query = r.json()

    if verbose:
        print(json_query['id'])
        print('JSON File created')

    return json_query


def get_gnd_keywordRelations(keywords: list, max_query_items=10, print_output=True, verbose=True, as_list=True,
                             max_keyword_relations=3, remove_duplicates=True,
                             json_keys=['relatedTerm', 'gndSubjectCategory', 'relatedPlaceOrGeographicName',
                                        'preferredName', 'broaderTermInstantial', 'broaderTermGeneral',
                                        'variantName']):
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

    df = pd.DataFrame()

    for keyword in keywords:
        json_query = get_gnd_json(query=keyword)

        try:
            total_items = len(json_query['member'])
        except:
            print(f'No items for keyword "{keyword}".')
            continue

        n_items = min(total_items, max_query_items)
        df[keyword] = [{json_key: list() for json_key in json_keys}]

        for item in range(n_items):

            member = json_query['member'][item]

            # get related Terms
            for json_key in json_keys:

                try:
                    for element in member[json_key]:
                        related_terms = element['label']

                        for term in related_terms.split(','):
                            stripped_term = term.strip(' ')
                            df[keyword][0][json_key].append(stripped_term)

                            if verbose:
                                print(
                                    f'Related Term for keyword "{keyword}" is {stripped_term}')

                except:

                    # If value of key is a list or string! No explicit label key
                    try:

                        for term in member[json_key].split(','):
                            stripped_term = term.strip(' ')
                            df[keyword][0][json_key].append(stripped_term)

                            if verbose:
                                print(
                                    f'Related Term for keyword "{keyword}" is {stripped_term}')

                    except:

                        try:

                            for term in member[json_key]:
                                df[keyword][0][json_key].append(term)

                                if verbose:
                                    print(
                                        f'Related Term for keyword "{keyword}" is {term}')

                        except:

                            if verbose:
                                print(
                                    f'Member {item+1} of kewyowrd "{keyword}" has no {json_key}.')

                if not as_list and remove_duplicates:
                    df[keyword][0][json_key] = list(
                        dict.fromkeys(df[keyword][0][json_key]))
                
                df[keyword][0][json_key] = [word.split(' ')[0].strip(';/:"') for word in df[keyword][0][json_key]]

        if as_list:
            keyword_relation_list = get_relevant_relations_as_list(df[keyword][0], keyword=keyword,
                                                                verbose=verbose,
                                                                max_keyword_relations=max_keyword_relations)
            df[keyword][0] = keyword_relation_list

        if print_output:
            print()
            print(f'---------- GND OUTPUT: {keyword}  ----------')
            print(df[keyword][0])

    return df


def get_relevant_relations_as_list(df: dict, keyword: str, verbose=False, max_keyword_relations=3):
    """
        The get_relevant_relations_as_list function accepts a dictionary with all related words and transforms 
        it to a single set with the most partnered words.

        :param df :dict: Used to pass the dictionary for each keyword.
        :param keyword: Used to pass keyword of our query.
        :param max_keyword_relations=3: Used to define the maximal number of words of the outputted list.
        :param verbose=False: Used to print out relevant information for debugging.
        :return: A list.
    """
    
    keyword_token = nlp(keyword)
    keyword_relation_set = set()
    keyword_similarities = []
    
    # Convert dictionary to simple list
    for key, relation_list in df.items():

        for word in relation_list:
            if word != keyword:
                keyword_relation_set.add(word)
    
    if len(keyword_relation_set) > 0:
    
        for i, word in enumerate(keyword_relation_set):
            keyword_similarities.append(keyword_token.similarity(nlp(word)))
        
        
        for k in range(3):
            try:
                keyword_relation_list = list(zip(*sorted(zip(keyword_relation_set, keyword_similarities), reverse=True)[:max_keyword_relations]))[0]
                break
            except IndexError:
                max_keyword_relations -= 1
    
    else:
        keyword_relation_list = ()

    if verbose:
        print('keyword_relation_list:', keyword_relation_list)

    return keyword_relation_list


def df_to_dict(df):
    df_dict = {}
    for i in range(df.shape[1]):
        df_dict[df.columns[i]] = list(filter(None, df.iloc[0, i]))
    return df_dict


if __name__ == '__main__':
    # TEST
    keys = ['Arbeiter', 'Arbeitgeber', 'Gasarbeiter',
            'Betriebe', 'auszumachen', 'streiken']
    df = get_gnd_keywordRelations(keywords=keys, max_query_items=200, print_output=True, verbose=False,
                                  max_keyword_relations=5)

    [print(f'{df.columns[i]} : {df.iloc[0,i]}') for i in range(df.shape[1])]
    print(df.shape)
