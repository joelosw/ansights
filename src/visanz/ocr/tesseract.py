# Imports
import pytesseract
from PIL import Image
from spellchecker import SpellChecker
from textblob import TextBlob
import sys
import os
sys.path.append('./')
sys.path.append('./../..')
if True:
    from src.visanz.utils.__RepoPath__ import repo_path
    from src.visanz.utils.logger import get_logger
logger = get_logger('OCR')

# 'data/2013_0473_031__ansicht03.tif'
# 'data/2013_0473_029__ansicht01.tif'
TEST_PATH = os.path.join(repo_path, 'data/2013_0473_023__ansicht01.tif')


def get_string(IMAGE_PATH, lang='deu_frak'):
    # Simple image to string
    text = pytesseract.image_to_string(
        Image.open(IMAGE_PATH), lang=lang)

    logger.debug(f'Tesseract extracted: \n {text}')

    return text


def get_string_from_image(image, lang='deu-frak'):
    # Simple image to string
    text = pytesseract.image_to_string(image, lang=lang)

    logger.debug(f'Tesseract extracted: \n {text}')

    return text


def init_SpellChecker():
    spell = SpellChecker('de')
    return spell


def enhance_text(spell, text_cleaned, debug=False):
    text_preprrocessed = ''

    for word in text_cleaned.split():
        if debug:
            logger.debug(word)

        # find those words that may be misspelled
        if spell.unknown([word]) != set():

            if debug:
                logger.debug(spell.candidates(word))

            word_variant = word.replace("f", "s")
            word_variant = word_variant.replace("F", "S")

            if spell.known([word_variant]) != set():
                text_preprrocessed = text_preprrocessed + word_variant + ' '
                continue

            text_preprrocessed = text_preprrocessed + \
                spell.correction(word) + ' '
        else:
            text_preprrocessed = text_preprrocessed + word + ' '
    return text_preprrocessed


def get_text_dict(languages=['deu_frak'], IMAGE_PATH=TEST_PATH, debug=False):
    text_strings = {}
    for lang in languages:
        logger.debug(f'===== LANGUAGE: {lang} =========')
        text = get_string(IMAGE_PATH=IMAGE_PATH, lang=lang, debug=debug)
        logger.debug(f'----Pure Text----- \n {text}')
        text_cleaned = clean_text(text)
        logger.debug(f'----Cleaned Text----- \n {text_cleaned}')
        spell = init_SpellChecker()
        text_preprocessed = enhance_text(
            spell=spell, text_cleaned=text_cleaned, debug=debug)
        logger.debug(f'----Final Text----- \n {text_preprocessed}')
        text_strings[lang] = text_preprocessed

    return text_strings


if __name__ == '__main__':
    get_text_dict(
        languages=['deu_frak'], IMAGE_PATH=TEST_PATH, debug=False)
