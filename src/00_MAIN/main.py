import sys
import os
import argparse
import pickle
sys.path.append('./')
sys.path.append('./../')
sys.path.append('./../..')
if True:
    from src.utils.__RepoPath__ import repo_path
    from src.utils.logger import get_logger
    from tesseract import get_string
    from fuse_keywords import fuse
    from lobid_api import get_gnd_keywordRelations, df_to_dict
    from build_newspaper_relations import build_relations, build_relations_with_synonyms
    from visualize_tfidf import VisAnz_Net
logger = get_logger('MAIN')

TEST_PATH = os.path.join(repo_path, 'data/2013_0473_023__ansicht01.tif')


def main(args: argparse):
    if not args.cache:
        ocr_text = get_string(TEST_PATH, lang='deu_frak')
        logger.info('OCR returned text: %s' % ocr_text)
        keywords_with_score = fuse(ocr_text, max_nouns=4, max_verbs=2)
        keywords = list(keywords_with_score.keys())
        logger.info(f'Extracted Keywords: {keywords}')

        if args.gnd:
            keywords_extended = df_to_dict(get_gnd_keywordRelations(keywords=keywords, max_query_items=30, print_output=False, verbose=False,
                                                                    max_keyword_relations=1))
            logger.info(f'GND-Extended Keywords: {keywords_extended}')
            relations = build_relations_with_synonyms(keywords_extended).values()
            #raise Warning('GND-Extended seaerch currently not enabled')
        else:
            relations = build_relations(keywords).values()
        logger.info(
            f'Main Programm finnishing with {len(relations)} results: \n {relations}')
        
        with open('relations-cache.pkl', 'wb') as f:
            pickle.dump(list(relations), f)
    
    else:
        with open('relations-cache.pkl', 'rb') as f:
            relations = pickle.load(f)
        
    vis_relations = {}
    vis_relations['id']=[]
    vis_relations['name']=[]
    vis_relations['context']=[]
    vis_relations['url']=[]
    vis_relations['keyword']=[]

    for i, value in enumerate(relations):
        vis_relations['id'].append(i)
        # TODO Heading aus der url rauslesen
        vis_relations['name'].append(' '.join(value.url.split('/')[-3:]))
        vis_relations['context'].append(value.context())
        vis_relations['url'].append(value.url)
        vis_relations['keyword'].append(next(iter(value.keywords)))
        
    data_keywords = ['test', 'test','test']
    visAnz_net = VisAnz_Net(data_dict=vis_relations, data_keywords=data_keywords)
    visAnz_net.show_net(PATH_NET='src/05_Visualization/Models/VisualAnzeights.html')


def parse_args():
    """Parse command line arguments."""
    desc = ('Execute main programm of Visual Anzeights')
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        '-f', '--file', type=str, required=False, default=TEST_PATH,
        help=('path to image to use'))
    parser.add_argument(
        '--gnd', action='store_true', required=False,
        help='Do not use GND to extend keywords')
    parser.add_argument('--cache', action='store_true', required=False)
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    logger.info('==== Starting Main Program =====')
    main(parse_args())
