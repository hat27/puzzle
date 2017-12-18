#-*- coding: utf8 -*-

import os
os.environ.setdefault("PUZZLE_MODULE_PATH", "somewhere")

__author__ = "Gou.Hattori"
__version__ = "0.0.1"

from . import env
from . import config
from . import Log
from . import Piece
from . import Puzzle