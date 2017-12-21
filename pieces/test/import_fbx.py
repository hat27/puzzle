#-*- coding: utf8 -*-
import os

from puzzle.Piece import Piece

_PIECE_NAME_ = "ImportFBX"

class ImportFBX(Piece):
    def __init__(self, **args):
        super(ImportFBX, self).__init__(**args)
        self.name = _PIECE_NAME_

    def execute(self):
        message = None
        message = None
        if not self.filtered:
            self.logger.debug("filtered")
            return True, self.pass_data, message        

        message = "import fbx: %s" % self.data["fbx_path"]
        self.logger.debug(message)
        
        return True, self.pass_data, message
