#! python3
"""
Main Files that includes different main functions depending on where it is called from
"""
import os
import argparse
import pickle
import webbrowser
import time
import logging
from types import SimpleNamespace
import sys
from datetime import date
from typing import Optional, Union, Any
from PIL import Image
sys.path.append('./')
sys.path.append('./..')
sys.path.append('./../..')

if True:
    from src.visanz.visualization.visualize_tfidf import VisAnz_Net
    from src.visanz.reichsanzeiger.news_page import News_Page
    from src.visanz.reichsanzeiger.build_newspaper_relations import build_relations, build_relations_with_synonyms, build_relations_async, build_relations_with_synonyms_async
    from src.visanz.gnd.lobid_api import get_gnd_keywordRelations, df_to_dict
    from src.visanz.ner.fuse_keywords import fuse
    from src.visanz.ocr.tesseract import get_string, get_string_from_image
    from src.visanz.utils.logger import get_logger
    from src.visanz.utils.__RepoPath__ import repo_path
    from src.visanz.visualization.keyword_visual import create_graph, generate_graph_content

# Set logging levels of single loggers as  wished
logger = get_logger('MAIN')
get_logger('ASYNC').setLevel(logging.INFO)
get_logger('KEY_VIS').setLevel(logging.INFO)
get_logger('REL').setLevel(logging.INFO)
get_logger('FESS').setLevel(logging.INFO)
get_logger('OCR').setLevel(logging.INFO)
TEST_PATH = os.path.join(repo_path, 'data/2013_0473_023__ansicht01.tif')
HTML_PATH = os.path.join(
    repo_path, 'src/visanz/visualization/VisualAnzeights.html')


def main(args: argparse, return_graph: bool = False, image: Union[Image, str] = None) -> Union[Any, None]:
    """
    Primary main method that runs each step one by one and passes the results to the next steps

    Parameters
    ----------
    args : argparse
        all thhe necessary arguments in a namespace, such as DateRange, Complexity, ...
    return_graph : bool, optional
        wether to return the generated graph, by default False
    image : Union[Image, str], optional
        Image to process, either PIL or Path, by default None

    Returns
    -------
    Union[Any, None]
        either returns the Graph or nothing
    """
    if not args.cache:
        if image is None or isinstance(image, str):
            ocr_text = get_string(args.file, lang='deu_frak')
        else:
            ocr_text = get_string_from_image(image, lang='deu_frak')
        logger.info('OCR returned text: \n %s' % ocr_text)
        keywords_with_score = fuse(ocr_text, max_nouns=4, max_verbs=3)
        keywords = list(keywords_with_score.keys())
        logger.info(f'Extracted Keywords: {keywords}')

        if args.gnd:
            keywords_extended = df_to_dict(get_gnd_keywordRelations(keywords=keywords, max_query_items=5, print_output=False, verbose=False,
                                                                    max_keyword_relations=1))
            logger.info(f'GND-Extended Keywords: {keywords_extended}')
            if args.parallel:
                t1 = time.time()
                relations = build_relations_with_synonyms_async(
                    keywords_extended, 10, args.sample)
                logger.info(
                    f'Building async GND-relations took {time.time() - t1} seconds')
            else:
                t1 = time.time()
                relations = build_relations_with_synonyms(
                    keywords_extended)
                logger.info(
                    f'Building sequential relations took {time.time() - t1} seconds')
            # raise Warning('GND-Extended seaerch currently not enabled')
        else:
            if args.parallel:
                t1 = time.time()
                relations = build_relations_async(
                    keywords, args.sample)
                logger.info(
                    f'Building async relations took {time.time() - t1} seconds')
            else:
                t1 = time.time()
                relations = build_relations(keywords)
                logger.info(
                    f'Building sequential relations took {time.time() - t1} seconds')

        logger.info(
            f'Main Programm finnishing with {len(relations)} results')

        with open('relations-cache.pkl', 'wb') as f:
            pickle.dump(list(relations), f)
            logger.info('Wrote relations to cache')

    else:
        with open('relations-cache.pkl', 'rb') as f:
            relations = pickle.load(f)
            logger.info(f'Loaded cached relations: {relations}')
    logger.info(f'Got {len(relations)} relations')
    year_l, year_h = tuple(
        args.dateRange) if args.dateRange else (1800, 1950)
    lower = date(
        year=year_l, month=1, day=1)
    upper = date(
        year=year_h, month=12, day=31)
    for article in relations:
        if not (lower <= article.date <= upper):
            relations.remove(article)
    logger.info(
        f'Filtered for years {lower} - {upper}: {len(relations)} relations')

    net = create_graph(relations, color_keywords=True)

    if return_graph:
        return net
    else:
        net.show_net(
            PATH_NET=HTML_PATH)
        webbrowser.open('file://' + HTML_PATH, new=0, autoraise=True)


def main_for_flask(image: Union[Image, str], **kwargs) -> tuple:
    """
    Wrapper  for  main method that can be called by th flask app.

    Parameters
    ----------
    image : Union[Image, str]

    Returns
    -------
    tuple
        nodes, edges, options for vis.js
    """
    logger.info(
        f'main_for_flask got image of type {type(image)} wit kwargs={kwargs}')
    args = SimpleNamespace(cache=False, parallel=True,
                           sample=kwargs['complexity'], keyvis=True, gnd=kwargs['gnd'], dateRange=kwargs['dateRange'])
    net = main(args, return_graph=True, image=image)
    nodes, edges, options = generate_graph_content(net)
    logger.info(
        f'Main for Flask finished, shapes: nodes:{len(nodes)}, edges:{len(edges)}, options:{len(options)}')
    return nodes, edges, options


def parse_args():
    """Parse command line arguments."""
    desc = ('Execute main programm of Visual Anzeights')
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        '-f', '--file', type=str, required=False, default=TEST_PATH,
        help=('path to image to use'))
    parser.add_argument('-g',
                        '--gnd', action='store_true', required=False,
                        help='Do not use GND to extend keywords')
    parser.add_argument('-c', '--cache', action='store_true', required=False,
                        help='If the program was run recently, the last query was cached, so that it is not necessary to do the full process again. ' +
                        'Instead just use the results from the last query')
    parser.add_argument('-p', '--parallel', '-a', '--async', action='store_true', required=False,
                        help='Use AsyncIOHttp to parallelize requests to the Reichsanzeiger FESS-API')
    parser.add_argument('--keyvis', action='store_true', required=False,
                        help='Use Common Keywords to calculate distance between nodes')
    parser.add_argument('-s', '--sample', type=int, required=False,
                        help='Use only a sample of possible keyword queries. This allows for multi-length queries')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    logger.info('==== Starting Main Program =====')
    main(parse_args())
