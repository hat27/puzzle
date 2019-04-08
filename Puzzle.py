# -*- coding: utf8 -*-

import os
import sys

import copy
import datetime
import traceback
import importlib
import logging
import subprocess

from . import PzLog
from . import pz_env as pz_env
from . import pz_config as pz_config


class Puzzle(object):
    def __init__(self, name="puzzle", file_mode=False, **args):
        """
        :type name: unicode
        :type file_mode: bool

        :param name: log name
        :param file_mode:  use environ to run
        :param args[use_default_config]:  use_default_config
        :param logger:  if logger in args, use it
        """
        self.file_mode = file_mode
        self.break_ = False
        self.pass_data = {}
        if self.file_mode:
            log_directory = os.environ.get("__PUZZLE_LOGGER_DIRECTORY__", pz_env.get_log_directory())
            self.name = os.environ.get("__PUZZLE_LOGGER_NAME__", name)
        else:
            log_directory = args.get("log_directory", pz_env.get_log_directory())
            self.name = name

        self.order = args.get("order", ["primary", "main", "post"])

        if not args.get("logger", False):
            self.Log = PzLog.PzLog(name=self.name,
                                                 new=args.get("new", False),
                                                 log_directory=log_directory,
                                                 use_default_config=args.get("use_default_config", False))

            self.logger = self.Log.logger
        else:
            self.logger = args["logger"]
        
        for handler in self.logger.handlers[::-1]:
            if hasattr(handler, "baseFilename"):
                self.logger.debug("baseFilename: {}".format(handler.baseFilename))

        pieces_directory = args.get("pieces_directory", False)
        if pieces_directory:
            if pieces_directory not in sys.path:
                sys.path.append(pieces_directory)

        if self.file_mode:
            self.play_as_file_mode()
            self.logger.debug("puzzle: play mode")
        else:
            self.logger.debug("puzzle: normal mode")

    @staticmethod
    def is_file_mode():
        if os.environ.get("__PUZZLE_FILE_MODE__", False):
            return True
        return False

    def force_close(self):
        flg = True
        message_ = "force close"

        try:
            import maya.cmds as cmds
            import maya.mel as mel
            mode = "maya"
        except:
            mode = "win"
        if mode == "maya":
            try:
                mel.eval('scriptJob -cf "busy" "quit -f -ec 0";')
                message_ = u"file app close: maya"
                flg = True
            except:
                message_ = u"file app close failed: maya"
                flg = False

        return flg, message_

    def play_as_file_mode(self):
        pz_path = os.environ["__ALL_PIECES_PATH__"]
        keys = os.environ["__PIECES_KEYS__"]
        data_path = os.environ["__PUZZLE_DATA_PATH__"]
        pass_path = os.environ.get("__PUZZLE_PASS_PATH__", "")
        pieces_directory = os.environ.get("__PUZZLE_HOOKS__", False)
        if pieces_directory:
            if pieces_directory not in sys.path:
                sys.path.append(pieces_directory)

        info, data = pz_config.read(data_path)
        pz_info, pz_data = pz_config.read(pz_path)

        if pass_path != "":
            pass_info, pass_data = pz_config.read(pass_path)
        else:
            pass_data = None
        keys = [l.strip() for l in keys.split(";") if l != ""]
        messages = []
        for key in keys:
            message = self.play(pz_data[key],
                                            data,
                                            pass_data)

            messages.extend(message)

        for message in messages:
            if not message[0]:
                self.close_event(messages)
                break

        return messages

    def close_event(self, messages):
        message_path = os.environ.get("__PUZZLE_MESSAGE_OUTPUT__", False)
        if message_path:
            pz_config.save(message_path, messages)

        if os.environ.get("__PUZZLE_CLOSE_APP__", False):
            self.force_close()

    def play(self, pieces, data, pass_data):
        def _play(piece_data_, data_, common_, part_, pass_data_):
            if isinstance(data_, list):
                messages_ = []
                flg_ = True
                if len(data_) == 0 and len(common_) > 0:
                    data_ = [common_]

                for i, d in enumerate(data_):
                    if self.break_:
                        return False, pass_data_, u"puzzle process stopped"

                    flg_, pass_data_, message_ = _play(piece_data_=piece_data_,
                                                        data_=d,
                                                        common_=common_,
                                                        part_=part_,
                                                        pass_data_=pass_data_)

                    messages_.extend(message_)

                    if not flg_:
                        self.break_ = True

                return flg_, pass_data_, messages_
            else:
                messages_ = []
                temp_common = copy.deepcopy(common)
                temp_common.update(data_)
                data_ = temp_common
                for piece_data_ in pieces.get(part_, []):
                    if self.break_:
                        message_ = [False,
                                    piece_data_.get("name", ""),
                                    piece_data_.get("description", ""),
                                    u"puzzle process stopped",
                                    u"puzzle process stopped"]

                        messages_.append(message_)
                        return False, pass_data_, messages_

                    flg_, pass_data_, header_, detail_ = self.fit(piece_data=piece_data_,
                                                                  data=data_,
                                                                  pass_data=pass_data_)

                    if header_ is not None:
                        message_ = [flg_,
                                    piece_data_.get("name", ""),
                                    piece_data_.get("description", ""),
                                    header_,
                                    detail_]

                        messages_.append(message_)
                    if not flg_:
                        self.break_ = True
                        return flg_, pass_data_, messages_

                return True, pass_data_, messages_
        
        self.break_ = False
        inp = datetime.datetime.now()
        messages = []
        self.logger.debug("start\n")
        common = data.get("common", {})
        for part in self.order:
            if part not in pieces:
                self.logger.debug("")
                continue

            data.setdefault(part, {})
            self.logger.debug("{}:".format(part))
            flg, self.pass_data, message = _play(piece_data_=pieces[part],
                                                                    data_=data[part],
                                                                    common_=common,
                                                                    part_=part,
                                                                    pass_data_=self.pass_data
                                                                    )
            if isinstance(message, list):
                messages.extend(message)
            else:
                messages.append(message)
            
            self.logger.debug("")

        if "finally" in pieces:
            self.break_ = False
            self.pass_data["messages"] = messages
            flg, self.pass_data, message = _play(piece_data_=pieces["finally"],
                                                                    data_={},
                                                                    common_=common,
                                                                    part_="finally",
                                                                    pass_data_=self.pass_data)

        self.logger.debug("takes: %s" % str(datetime.datetime.now() - inp))
        self.close_event(messages)

        return messages

    def fit(self, piece_data, data, pass_data):
        hook_name = piece_data["piece"]
        header = ""
        detail = ""
        try:
            self.logger.debug(hook_name)
            print
            mod = importlib.import_module(hook_name)
            reload(mod)
            if hasattr(mod, "_PIECE_NAME_"):
                mod = getattr(mod, mod._PIECE_NAME_)(piece_data=piece_data,
                                                     data=data,
                                                     pass_data=pass_data,
                                                     logger=self.logger)
            else:
                return False, pass_data, header, detail
            inp = datetime.datetime.now()
            if not mod.filtered:
                return True, pass_data, None, detail
            
            self.logger.debug(hook_name)
            results = mod.execute()
            self.logger.debug("{}\n".format(datetime.datetime.now() - inp))
            return results

        except:
            self.logger.debug(traceback.format_exc())
            print traceback.format_exc()
            return False, pass_data, header, traceback.format_exc()
