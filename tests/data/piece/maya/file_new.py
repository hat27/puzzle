import sys
import os
import inspect

module_path = os.environ.get("PUZZLE_REPO_PATH")
if module_path:
    sys.path.append(module_path)

from puzzle.Piece import Piece
import maya.cmds as cmds

_PIECE_NAME_ = "FileNew"

from puzzle.Piece import Piece
class FileNew(Piece):
    def __init__(self, **args):
        super(FileNew, self).__init__(**args)
        self.name = _PIECE_NAME_

    def execute(self):
        self.header = "file new"

        try:
            cmds.file(new=True, f=True)
            self.details.append("file new")
            flg = True

        except:
            self.details.append("file new failed")
            flg = False

        return flg, self.pass_data, self.header, self.details

if __name__ == "__main__":
    x = FileNew()
    print(x.execute())
    