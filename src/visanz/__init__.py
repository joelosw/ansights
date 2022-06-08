from pkgutil import extend_path
import sys
import os
__path__ = extend_path(__path__, __name__)
__path__ = extend_path(__path__, 'main')
__path__ = extend_path(__path__, 'ocr')
this_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(this_path, 'ocr'))
sys.path.append(os.path.join(this_path, 'ner'))
sys.path.append(os.path.join(this_path, 'gnd'))
sys.path.append(os.path.join(this_path, 'reichsanzeiger'))
sys.path.append(os.path.join(this_path, 'visualization'))
