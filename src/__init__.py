from pkgutil import extend_path
import sys
import os
__path__ = extend_path(__path__, './01_OCR')
__path__ = extend_path(__path__, __name__)
this_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(this_path, '01_OCR'))
sys.path.append(os.path.join(this_path, '02_NER'))
sys.path.append(os.path.join(this_path, '03_GND'))
sys.path.append(os.path.join(this_path, '04_Reichsanzeiger'))

