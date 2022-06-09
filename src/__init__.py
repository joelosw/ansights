from pkgutil import extend_path
import sys
import os
this_path = os.path.dirname(os.path.realpath(__file__))
__path__ = extend_path(__path__, __name__)
__path__ = extend_path(__path__, 'visanz')
sys.path.append(os.path.join(this_path, 'flask_backend'))
sys.path.append(os.path.join(this_path, 'visanz'))
