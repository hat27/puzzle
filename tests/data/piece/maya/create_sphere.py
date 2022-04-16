import sys
import os
import inspect

module_path = os.environ.get("PUZZLE_REPO_PATH")
if module_path:
    sys.path.append(module_path)

from puzzle.Piece import Piece
import maya.cmds as cmds

_PIECE_NAME_ = "CreateSphere"

from puzzle.Piece import Piece
class CreateSphere(Piece):
    def __init__(self, **args):
        super(CreateSphere, self).__init__(**args)
        self.name = _PIECE_NAME_

    def execute(self):
        self.logger.info("this is info level log")
        self.header = "create shpere"
        x = cmds.polySphere(name=self.data["name"])
        if "move" in self.data:
            cmds.move(*self.data["move"])
            self.logger.debug("move: {}".format(self.data["move"]))

        return True, self.pass_data, self.header, self.details

if __name__ == "__main__":
    data = {"name": "hoge"}
    x = CreateSphere(data=data)
    print(x.execute())
    