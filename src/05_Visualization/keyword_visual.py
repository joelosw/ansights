from pyvis.network import Network
import sys
import numpy as np
import webbrowser
import os
import cv2
sys.path.append('./')
sys.path.append('./../')
sys.path.append('./../..')
if True:  # necesarry, so that auto-format does not move the import to top
    from src.utils.__RepoPath__ import repo_path
    from src.utils.logger import get_logger
    from news_page import News_Page
logger = get_logger('KEY_VIS')


def calculate_similarity_matrix(news_pages, eps=1):
    similarities = np.zeros((len(news_pages), len(news_pages)))
    for i in range(len(news_pages)):
        for j in range(i):
            similarities[i, j] = len(news_pages[i].common_keywords(
                news_pages[j])) + eps
            logger.debug(f'Dist between {i},{j} = {similarities[i,j]}')

    return similarities


def create_graph(news_pages, physics=True, paper=None, num_keywords=6):
    #similarities = calculate_similarity_matrix(news_pages, eps=0.1)
    net = Network(height='100%', width='75%')
    net.barnes_hut()
    if not paper is None:
        net.add_node('KEY', size=10*num_keywords, title='Flugblatt', label='Flugblatt', shape='image',
                     image='file:///Users/joel/Library/CloudStorage/OneDrive-Personal/_UNI/SS22/daVinci/data/example_flyer.jpg')
    for i, page in enumerate(news_pages):
        net.add_node(i, size=10*len(page.keywords),
                     title=page.url, label=page.name.split('-')[-1], shape='image', image='file:////Users/joel/Library/CloudStorage/OneDrive-Personal/_UNI/SS22/daVinci/data/example_scan.jpg')
        net.add_edge('KEY', i, weight=len(page.keywords), value=len(
            page.keywords), smooth=False, title=','.join(page.keywords), color='darkblue')
    for i in range(len(news_pages)):
        for j in range(i):
            #similarity = similarities[i, j]
            # net.add_edge(i, j, weight=dist, value=dist,
            #              length=(100*np.max(similarities)/dist), physics=physics)
            common_words = news_pages[i].common_keywords(news_pages[j])
            similarity = len(common_words)
            if similarity > 0:
                net.add_edge(i, j, weight=similarity,
                             value=similarity, smooth=False, title=','.join(common_words))
    return net


def add_paper_to_net():
    pass


if __name__ == '__main__':
    import pickle
    import random
    with open('relations-cache.pkl', 'rb') as f:
        relations = pickle.load(f)
        logger.info(
            f'{relations} \n  ...loaded cached {len(relations)} relations:')
    relations = random.sample(relations, 30)
    net = create_graph(relations, paper=True)
    net.show(os.path.join(repo_path, 'key_vis.html'))
    webbrowser.open('file://' + os.path.join(repo_path,
                    'key_vis.html'), new=0, autoraise=True)
