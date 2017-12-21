#-*- coding: utf8 -*-
import os

from puzzle.Piece import Piece

_PIECE_NAME_ = "SaveFile"

class SaveFile(Piece):
    def __init__(self, **args):
        super(SaveFile, self).__init__(**args)
        self.name = _PIECE_NAME_

    def execute(self):
        message = None
        if not self.filtered:
            self.logger.debug("filtered")
            return True, self.pass_data, message
        
        if True:
            message = u"file saved: %s" % self.data["save_path"]
            self.logger.debug(message)
        else:
            message = u"file save failed: %s" % self.data["save_path"]
            self.logger.debug(message)

        return True, self.pass_data, message
