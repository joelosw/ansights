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
    from src.visanz.ner.spacy_test import extract_ner
    from src.visanz.ocr.tesseract import get_string, get_string_from_image
    from src.visanz.utils.logger import get_logger
    from src.visanz.utils.__RepoPath__ import repo_path
    from src.visanz.visualization.keyword_visual import create_graph, generate_graph_content

FLYER_PATH = os.path.join(repo_path, 'data/flyer')
CSV_PATH = os.path.join(repo_path, 'data/knowledge_graph.csv')

ids = os.listdir(FLYER_PATH)
# Only use jpgs
ids = [i for i in ids if i.endswith('.jpg')]

for id in tqdm(ids):
    with open(CSV_PATH, 'a') as csv:
        print(f'=====Looking at {id}')
        path = os.path.join(FLYER_PATH, id)
        text = get_string(path, lang='deu_frak').replace('\n', " ")
        ner = extract_ner(text)
        keywords_with_score = fuse(text, max_nouns=4, max_verbs=3)
        keywords = list(keywords_with_score.keys())
        scores = list(keywords_with_score.values())
        keywords_extended = df_to_dict(get_gnd_keywordRelations(keywords=keywords, max_query_items=30, print_output=False, verbose=False,
                                                                max_keyword_relations=3))
        print(f'-------NER result: {ner}---------')
        row = id + ','

        keywords_to_add = [str(i)
                           for i in keywords_with_score.items()]
        row += ',Spacy+Yake,'.join(keywords_to_add) + \
            (',Spacy+Yake,' if len(keywords_to_add) > 0 else '')

        synonyms_to_add = [str(i)
                           for i in keywords_extended.values() if len(i) > 0]
        row += ',GNDSynonyms,'.join(synonyms_to_add) + \
            (',GNDSynonyms,' if len(synonyms_to_add) > 0 else '')

        ner_to_add = [f'{v}:"{k}"'.replace('\n', ' ')
                      for k, v in ner.items() if not v == 'MISC']
        row += ',NER,'.join(ner_to_add) + \
            (',NER,' if len(ner_to_add) > 0 else ' ')
        row = row.strip(',')
        csv.write(row+'\n')
