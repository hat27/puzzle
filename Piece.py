#-*- coding: utf8 -*-

import copy
class Piece(object):
    def __init__(self, **args):
        #self.data = args["data"]
        self.data = copy.deepcopy(args["data"])
        self.pass_data = args["pass_data"]
        self.piece_data = args["piece_data"]
        self.logger = args["logger"]
        if "paint" in self.piece_data:
            for k, v in self.piece_data["paint"].items():
                if v in self.data:
                    self.data[k] = self.data[v]
                    del self.data[v]
        self.message = ""
        self.filtered = True
        if "filters" in self.piece_data:
            for filter_ in self.piece_data["filters"]:
                for k, v in filter_.items():
                    if not k in self.data:
                        self.filtered = False
                        break
                    if isinstance(v, list):
                        if not self.data[k] in v:
                            self.filtered = False
                    else:
                        if v != self.data[k]:
                            self.filtered = False


    def execute(self, **args):
        return True, self.pass_data, self.message
