from PIL import Image
from cleantext import clean
from spellchecker import SpellChecker

import pytesseract

TEST_PATH = '../../data/2013_0473_031__ansicht03.tif'

# If you don't have tesseract executable in your PATH, include the following:
pytesseract.pytesseract.tesseract_cmd = r'tesseract'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

# Simple image to string
text = pytesseract.image_to_string(Image.open(TEST_PATH))
print(text[:100])

text_cleaned = clean(text[:100])
spell = SpellChecker('de')

# find those words that may be misspelled
# misspelled = spell.unknown(text_cleaned.split())
text_prep = ''

for word in text_cleaned.split():
    # Get the one `most likely` answer
    print(word)
    print(spell.unknown(word))
    if spell.unknown(word) != spell.unknown('Bro'):
        print(spell.unknown(word))
        # print(spell.correction(word))
        text_prep = text_prep + spell.correction(word) + ' '
    else:
        text_prep = text_prep + word + ' '


    # Get a list of `likely` options
    # print(spell.candidates(word))

print(text_prep)



# Batch processing with a single file containing the list of multiple image file paths
# print(pytesseract.image_to_string('images.txt'))

# Timeout/terminate the tesseract job after a period of time
'''try:
    print(pytesseract.image_to_string(TEST_PATH, timeout=2)) # Timeout after 2 seconds
    print(pytesseract.image_to_string(TEST_PATH, timeout=0.5)) # Timeout after half a second
except RuntimeError as timeout_error:
    # Tesseract processing is terminated
    pass

# Get bounding box estimates
# print(pytesseract.image_to_boxes(Image.open(TEST_PATH)))

# Get verbose data including boxes, confidences, line and page numbers
# print(pytesseract.image_to_data(Image.open(TEST_PATH)))

# Get information about orientation and script detection
#print(pytesseract.image_to_osd(Image.open(TEST_PATH)))

# Get a searchable PDF
#pdf = pytesseract.image_to_pdf_or_hocr('test.png', extension='pdf')
#with open('test.pdf', 'w+b') as f:
    #f.write(pdf) # pdf type is bytes by default

# Get HOCR output
#hocr = pytesseract.image_to_pdf_or_hocr('test.png', extension='hocr')

# Get ALTO XML output
#xml = pytesseract.image_to_alto_xml('test.png')'''