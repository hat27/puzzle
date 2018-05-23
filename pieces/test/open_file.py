#-*- coding: utf8 -*-
import os

from puzzle.Piece import Piece

_PIECE_NAME_ = "OpenFile"

class OpenFile(Piece):
    def __init__(self, **args):
        super(OpenFile, self).__init__(**args)
        self.name = _PIECE_NAME_

    def execute(self):
        header = None
        detail = ""

        if self.data["open_path"] is None:
            self.logger.debug("open new")
            header = u"file open: new"
            detail = u""
        elif os.path.exists(self.data["open_path"]):
            header = u"file open: %s" % self.data["open_path"]
            self.logger.debug(header)
        else:
            header = u"file open: new"
            self.logger.debug(header)

        return True, self.pass_data, header, detail
