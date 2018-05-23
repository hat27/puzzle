#-*- coding: utf8 -*-
import os

from puzzle.Piece import Piece

_PIECE_NAME_ = "ReferenceChara"

class ReferenceChara(Piece):
    def __init__(self, **args):
        super(ReferenceChara, self).__init__(**args)
        self.name = _PIECE_NAME_

    def execute(self):
        header = None
        detail = None
        if not self.filtered:
            self.logger.debug("filtered")
            return True, self.pass_data, header, detail

        header = "chara referenced: %s" % self.data["asset_path"]
        self.logger.debug(header)
        return True, self.pass_data, header, detail
