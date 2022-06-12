import os
import sys
from tqdm import tqdm
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

PATH = os.path.join(repo_path, 'data/flyer')
CSV_PATH = os.path.join(repo_path, 'data/knowledge_graph.csv')

ids = os.listdir(PATH)
with open(CSV_PATH, 'a') as csv:
    for id in tqdm(ids):
        print(f'=====Looking at {id}')
        path = os.path.join(PATH, id)
        text = get_string(path, lang='deu_frak')
        keywords_with_score = fuse(text, max_nouns=4, max_verbs=3)
        keywords = list(keywords_with_score.keys())
        keywords_extended = df_to_dict(get_gnd_keywordRelations(keywords=keywords, max_query_items=30, print_output=False, verbose=False,
                                                                max_keyword_relations=3))

        csv.write(f'{id},'+','.join(keywords)+','.join(keywords_extended)+'\n')
