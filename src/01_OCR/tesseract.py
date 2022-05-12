# Imports
from PIL import Image
from cleantext import clean
from spellchecker import SpellChecker
from textblob import TextBlob

import pytesseract

# 'data/2013_0473_031__ansicht03.tif'
# 'data/2013_0473_029__ansicht01.tif'
TEST_PATH = 'data/2013_0473_031__ansicht03.tif'

# If you don't have tesseract executable in your PATH, include the following:
# pytesseract.pytesseract.tesseract_cmd = r'tesseract'
# print(pytesseract.get_languages(config=''))

def get_string(IMAGE_PATH, lang='deu',debug=False):
    # Simple image to string
    text = pytesseract.image_to_string(Image.open(IMAGE_PATH), lang=lang) # 'deu'
    # text = TextBlob(text)
    
    if debug:
        print(text)

    return text

def clean_text(text):
    text_cleaned = clean(text[:])
    return text_cleaned

def init_SpellChecker():
    spell = SpellChecker('de')
    return spell

def enhance_text(spell, text_cleaned, debug=False):
    text_preprrocessed = ''

    for word in text_cleaned.split():
        if debug:
            print(word)

        # find those words that may be misspelled
        if spell.unknown([word]) != set():
            
            if debug:
                print(spell.candidates(word))
            
            word_variant = word.replace("f", "s")
            word_variant = word_variant.replace("F", "S")

            if spell.known([word_variant]) != set():
                text_preprrocessed = text_preprrocessed + word_variant + ' '
                continue
            
            text_preprrocessed = text_preprrocessed + spell.correction(word) + ' '
        else:
            text_preprrocessed = text_preprrocessed + word + ' '

    print(text_preprrocessed)

def get_text_dict(languages=['deu', 'deu_frak'], IMAGE_PATH=TEST_PATH, debug=False):
    text_strings = {}
    for lang in languages:
        text = get_string(IMAGE_PATH=IMAGE_PATH, lang=lang,debug=debug)
        text_cleaned = clean_text(text)
        spell = init_SpellChecker()
        text_preprocessed = enhance_text(spell=spell, text_cleaned=text_cleaned, debug=debug)
        text_strings[lang] = text_preprocessed
    
    return text_strings

if __name__ == '__main__':
    get_text_dict(languages=['deu', 'deu_frak'], IMAGE_PATH=TEST_PATH, debug=False)