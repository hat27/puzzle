# -*-coding: utf8-*-

import os
import sys
import json

path = sys.argv[-1]
if not path.endswith(".json"):
    raise Exception(u"json not sets")

sys.path.append(os.environ["__PUZZLE_PATH__"])
sys.path.append("{}\\puzzle\\pieces\\app\\PzEndDialog".format(os.environ["__PUZZLE_PATH__"]))

from Qt import QtWidgets, QtCore, QtGui
from puzzle.pieces.app.PzEndDialog.main import PzDialog

js = json.load(open(path, "r"), "utf8")
app = QtWidgets.QApplication(sys.argv)
x = PzDialog(messages=js)
x.set_ui()
app.exec_()

