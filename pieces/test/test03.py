#-*- coding: utf8 -*-
import os

from puzzle.Piece import Piece

_PIECE_NAME_ = "Test03"

class Test03(Piece):
    def __init__(self, **args):
        super(Test03, self).__init__(**args)
        self.name = _PIECE_NAME_

    def execute(self):
        message = None
        if not self.filtered:
            self.logger.debug("filtered")
            return True, self.pass_data, message

        message = "prop referenced: %s" % self.data["asset_path"]
        self.logger.debug(message)

        return True, self.pass_data, message

