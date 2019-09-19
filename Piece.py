#-*- coding: utf8 -*-

import copy
from . import PzLog

class Piece(object):
    def __init__(self, **args):
        #self.data = args["data"]
        self.data = copy.deepcopy(args.get("data", {}))
        self.pass_data = args.get("pass_data", {})
        self.piece_data = args.get("piece_data", {})
        self.logger = args.get("logger", False)
        if not self.logger:
            log = PzLog.PzLog()
            self.logger = log.logger
        
        if "paint" in self.piece_data:
            """
            startwith @: check it from pass_data
            """
            for k, v in self.piece_data["paint"].items():
                if v.startswith("@"):
                    if v[1:] in self.pass_data:
                        self.data[k] = self.pass_data[v[1:]]

                elif v in self.data:
                    self.data[k] = self.data[v]
                    # del self.data[v]
        self.header = ""
        description = self.piece_data.get("description", "")
        self.details = []
        if description != u"":
            self.details = ["", u"【{}】".format(description), self.piece_data["piece"], ""]

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
        return True, self.pass_data, self.header, self.details