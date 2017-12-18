#-*- coding: utf8 -*-
import os

from puzzle.Piece import Piece

_PIECE_NAME_ = "Test01"

class Test01(Piece):
    def __init__(self, **args):
        super(Test01, self).__init__(**args)
        self.name = _PIECE_NAME_

    def execute(self):
        message = None
        if self.data["open_path"] is None:
            self.logger.debug("open new")
            message = u"file open: new"
        elif os.path.exists(self.data["open_path"]):
            message = u"file open: %s" % self.data["open_path"]
            self.logger.debug(message)
        else:
            message = u"file open: new"
            self.logger.debug(message)

        return True, self.pass_data, message
