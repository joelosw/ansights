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
tessdata_dir_config = r'--tessdata-dir "{}/data/tessdata"'.format(repo_path)


def get_string(IMAGE_PATH: str, lang: str = 'deu_frak') -> str:
    """Simple Image to text wrapper.

    Parameters
    ----------
    IMAGE_PATH : str

    lang : str, optional
         by default 'deu_frak':str

    Returns
    -------
    str
        Extracted text
    """
    text = pytesseract.image_to_string(
        Image.open(IMAGE_PATH), lang=lang, config=tessdata_dir_config)

    logger.debug(f'Tesseract extracted: \n {text}')

    return text


def get_string_from_image(image: Image, lang: str = 'deu_frak') -> str:
    """
    Simple IMage to text wrapper.

    Parameters
    ----------
    image : Image
            in PIL format

    lang : str, optional
            by default 'deu_frak':str

    Returns
    -------
    str
        Extracted text
    """
    text = pytesseract.image_to_string(
        image, lang=lang, config=tessdata_dir_config)

    logger.debug(f'Tesseract extracted: \n {text}')

    return text


def init_SpellChecker():
    spell = SpellChecker('de')
    return spell


def enhance_text(spell: SpellChecker, text_cleaned: str) -> str:
    """
    CLean the text a little. Does not work so great unfortunately.

    Parameters
    ----------
    spell : SpellChecker
        TO check wether word is spelled correct
    text_cleaned : str
        text that is to be checked

    Returns
    -------
    str
        processed text
    """
    text_preprrocessed = ''

    for word in text_cleaned.split():

        logger.debug(word)

        # find those words that may be misspelled
        if spell.unknown([word]) != set():

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


def get_text_dict(languages: list = ['deu_frak'], IMAGE_PATH: str = TEST_PATH) -> dict:
    """Run the OCR Pipeline for several language models. 
    Mainly for comparison and testinf

    Parameters
    ----------
    languages : list, optional
        by default ['deu_frak']
    IMAGE_PATH : str, optional
        where the image is stored, by default TEST_PATH

    Returns
    -------
    dict
        Dictionary with text entries for every language model
    """
    text_strings = {}
    for lang in languages:
        logger.debug(f'===== LANGUAGE: {lang} =========')
        text = get_string(IMAGE_PATH=IMAGE_PATH, lang=lang)
        logger.debug(f'----Pure Text----- \n {text}')
        spell = init_SpellChecker()
        text_preprocessed = enhance_text(
            spell=spell, text_cleaned=text)
        logger.debug(f'----Final Text----- \n {text_preprocessed}')
        text_strings[lang] = text_preprocessed

    return text_strings


if __name__ == '__main__':
    get_text_dict(
        languages=['deu_frak'], IMAGE_PATH=TEST_PATH)
