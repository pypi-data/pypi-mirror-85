"""ajgar.py: Main module.

"""
from __future__ import print_function, division, absolute_import
    
__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2016, Dilawar Singh"
__license__          = "GNU GPL"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"

from dilawar.core import *

try:
    # This depends on scipy
    from dilawar.data_analysis import *
except ImportError:
    pass

try:
    from dilawar.text_processing import *
except ImportError:
    pass

try:
    from dilawar.file_utils import *
except ImportError:
    pass

try:
    from dilawar.plot_utils import *
except ImportError:
    pass
try:
    from  dilawar.statistics import *
except ImportError:
    pass

try:
    from dilawar.io_utils import *
except ImportError:
    pass

try:
    from dilawar.logger import *
except ImportError:
    pass

try:
    from dilawar.information_theory import *
except ImportError:
    pass

try:
    from dilawar.functions import *
except ImportError:
    pass

try:
    import networkx as nx
    from dilawar.nx_utils import *
except Exception as e:
    pass

# NOTE: brian2 should not be imported by default. 
