name = "knockpy"
all = [
    "dgp",
    "knockoff_stats",
    "knockoff_filter",
    "knockoffs",
    "mac",
    "metro",
    "mrc",
    "smatrix",
    "tree_processing"
    "utilities",
]

from . import dgp
from . import knockoffs
from . import knockoff_filter
from . import knockoff_stats
from . import mac
from . import metro
from . import mrc
from . import smatrix
from . import tree_processing
from . import utilities

with open('../VERSION', 'r') as vh:
    __version__ = vh.read()