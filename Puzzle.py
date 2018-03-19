#-*- coding: utf8 -*-

import os
import sys
import datetime

import traceback
import importlib

from . import Log
from . import config as pz_config

class Puzzle(object):
    def __init__(self, name="puzzle", file_mode=False, **args):
        self.name = name
        self.order = args.get("order", ["primary", "main", "post"])
        self.Log = Log.Log(name=self.name, 
                           new=True, 
                           update_config=args.get("update_log_config", False))

        self.logger = self.Log.logger
        self.file_mode = file_mode
        self.end = False
        pieces_directory = args.get("pieces_directory", False)
        if pieces_directory:
            if not pieces_directory in sys.path:
                sys.path.append(pieces_directory)

        if self.file_mode:
            self.play_as_file_mode()

    def is_file_mode(self):
        if os.environ.get("__PUZZLE_FILE_MODE__", False):
            return True
        return False

    def play_as_file_mode(self):
        pz_path = os.environ["__ALL_PIECES_PATH__"]
        keys = os.environ["__PIECES_KEYS__"]
        data_path = os.environ["__PUZZLE_DATA_PATH__"]
        pass_path = os.environ.get("__PUZZLE_PASS_PATH__", "")
        log_name = os.environ.get("__PUZZLE_LOG_NAME__", "puzzle")

        info, data = pz_config.read(data_path)
        pz_info, pz_datas = pz_config.read(pz_path)
        if pass_path != "":
            pass_info, pass_data = pz_config.read(pass_path)
        else:
            pass_data = None

        keys = [l.strip() for l in keys.split(";") if l != ""]
        messages = []
        for key in keys:
            message = self.play(pz_datas[key], 
                                data, 
                                pass_data, 
                                log_name=log_name)

            messages.extend(message)
        return messages

    def play(self, pieces, data, pass_data, log_name="puzzle"):
        def _play(piece_data, data, part, pass_data, logger=None):
            if isinstance(data, list):
                messages = []
                for i, d in enumerate(data):
                    if self.end:
                        return False, pass_data, u"puzzle process stopped"

                    flg, pass_data, message = _play(piece_data=piece_data, 
                                                    data=d, 
                                                    part=part, 
                                                    pass_data=pass_data,
                                                    logger=logger
                                                    )
                    
                    messages.extend(message)
                    if not flg:
                        self.end = True

                return flg, pass_data, messages
            else:
                messages = []
                for piece_data in pieces.get(part, []):
                    if self.end:
                        return False, pass_data, u"puzzle process stopped"
                    flg, pass_data, message = self.fit(piece_data=piece_data, 
                                                       data=data,
                                                       pass_data=pass_data,
                                                       logger=logger
                                                       )
                    if not message is None:
                        message = [flg,
                                   piece_data.get("name", ""), 
                                   piece_data.get("description", ""),
                                   message]

                        messages.append(message)
                    if not flg:
                        self.end = True
                        return flg, pass_data, messages

                return True, pass_data, messages
        

        inp = datetime.datetime.now()
        messages = []
        self.logger.debug("start\n")
        for part in self.order:
            if not part in pieces:
                self.logger.debug("")
                continue
            common = data.get("common", {})
            data.setdefault(part, {})
            common.update(data[part])
            data[part] = common
            self.logger.debug("%s:" % part)
            flg, pass_data, message = _play(piece_data=pieces[part], 
                                            data=data[part], 
                                            part=part, 
                                            pass_data=pass_data,
                                            logger=self.logger
                                            )

            if isinstance(message, list):
                messages.extend(message)
            else:
                messages.append(message)
            
            self.logger.debug("")

        self.logger.debug("takes: %s" % str(datetime.datetime.now() - inp))
        return messages

    def fit(self, piece_data, data, pass_data, logger=None):
        hook_name = piece_data["piece"]
        message = ""
        try:
            mod = importlib.import_module(hook_name)
            reload(mod)
            logger.debug("name        : %s (%s)" % (piece_data["name"], hook_name))
            logger.debug("description : %s" % piece_data["description"])
            if hasattr(mod, "_PIECE_NAME_"):
                mod = getattr(mod, mod._PIECE_NAME_)(piece_data=piece_data, 
                                                     data=data, 
                                                     pass_data=pass_data,
                                                     logger=logger)
            else:
                return False, pass_data, message
            inp = datetime.datetime.now()
            results = mod.execute()
            logger.debug("%s\n" % str(datetime.datetime.now() - inp))
            return results
        except:
            logger.debug(traceback.format_exc())
            return False, pass_data, message