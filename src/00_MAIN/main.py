import sys
import os
import argparse
import pickle
import webbrowser
import time
import logging
from types import SimpleNamespace
sys.path.append('./')
sys.path.append('./../')
sys.path.append('./../..')
if True:  # necesarry, so that auto-format does not move the import to top
    from src.utils.__RepoPath__ import repo_path
    from src.utils.logger import get_logger
    from tesseract import get_string
    from fuse_keywords import fuse
    from lobid_api import get_gnd_keywordRelations, df_to_dict
    from build_newspaper_relations import build_relations, build_relations_with_synonyms, build_relations_async, build_relations_with_synonyms_async
    from news_page import News_Page
    from visualize_tfidf import VisAnz_Net
    from keyword_visual import create_graph, generate_graph_content
logger = get_logger('MAIN')
get_logger('ASYNC').setLevel(logging.INFO)
TEST_PATH = os.path.join(repo_path, 'data/2013_0473_023__ansicht01.tif')
HTML_PATH = os.path.join(
    repo_path, 'src/05_Visualization/Models/VisualAnzeights.html')
# TODO: Check wordnet for cleaning OCR  text (part of nltk?) -> Don't lemmatize
# TODO: Include spacy NER if found, statistics on FP/FN of NER
# TODO: Ask about limitations of FESS-API

# TODO: Clusteer Colors
# TODO: 10 newspaper-icons
# TODO: Onclick -> Link öffnen


def main(args: argparse, return_graph=False):
    if not args.cache:
        ocr_text = get_string(args.file, lang='deu_frak')
        logger.info('OCR returned text: %s' % ocr_text)
        keywords_with_score = fuse(ocr_text, max_nouns=4, max_verbs=3)
        keywords = list(keywords_with_score.keys())
        logger.info(f'Extracted Keywords: {keywords}')

        if args.gnd:
            keywords_extended = df_to_dict(get_gnd_keywordRelations(keywords=keywords, max_query_items=30, print_output=False, verbose=False,
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
    if not args.keyvis:
        vis_relations = {}
        vis_relations['id'] = []
        vis_relations['name'] = []
        vis_relations['context'] = []
        vis_relations['url'] = []
        vis_relations['keyword'] = []

        for i, value in enumerate(relations):
            vis_relations['id'].append(i)
            # TODO Heading aus der url rauslesen
            vis_relations['name'].append(' '.join(value.url.split('/')[-3:]))
            vis_relations['context'].append(value.context())
            vis_relations['url'].append(value.url)
            vis_relations['keyword'].append(next(iter(value.keywords)))

        data_keywords = ['test', 'test', 'test']
        net = VisAnz_Net(data_dict=vis_relations,
                         data_keywords=data_keywords)
    else:
        net = create_graph(relations, color_keywords=True)

    if return_graph:
        return net
    else:
        net.show_net(
            PATH_NET=HTML_PATH)
        webbrowser.open('file://' + HTML_PATH, new=0, autoraise=True)


def main_for_flask(image, gnd: bool = True):
    args = SimpleNamespace(cache=False, parallel=True,
                           sample=30, keyvis=True, gnd=gnd)
    net = main(args, return_graph=True)
    nodes, edges, options = generate_graph_content(net)
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
