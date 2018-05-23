# -*- coding: utf8 -*-

import os
import sys



import datetime
import traceback
import importlib

from . import PzLog
from . import pz_config as pz_config
import subprocess


class Puzzle(object):
    def __init__(self, name="puzzle", file_mode=False, **args):
        """
        :type name: unicode
        :type file_mode: bool
        :param name: log name
        :param file_mode:  use environ to run
        :param args[update_log_config]:  update log config
        :param logger:  if logger in args, use it
        """
        self.file_mode = file_mode
        self.break_ = False
        self.pass_data = {}
        log_directory = False
        if self.file_mode:
            self.name = os.environ.get("__PUZZLE_LOGGER_NAME__", name)
            log_directory = os.environ.get("__PUZZLE_LOGGER_DIRECTORY__", False)
        else:
            self.name = name

        self.order = args.get("order", ["primary", "main", "post"])
        if not args.get("logger", False):
            self.Log = PzLog.PzLog(name=self.name,
                                 new=args.get("new", False),
                                 log_directory=log_directory,
                                 update_config=args.get("update_log_config", False))
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
        def _play(piece_data_, data_, part_, pass_data_):
            if isinstance(data_, list):
                messages_ = []
                for i, d in enumerate(data_):
                    if self.break_:
                        return False, pass_data_, u"puzzle process stopped"

                    flg_, pass_data_, message_ = _play(piece_data_=piece_data_,
                                                        data_=d,
                                                        part_=part_,
                                                        pass_data_=pass_data_)

                    messages_.extend(message_)

                    if not flg_:
                        self.break_ = True

                return flg_, pass_data_, messages_
            else:
                messages_ = []
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
        for part in self.order:
            if part not in pieces:
                self.logger.debug("")
                continue

            common = data.get("common", {})
            data.setdefault(part, {})
            if len(common) != 0:
                if isinstance(data[part], dict):
                    common.update(data[part])
                else:
                    print "?????????????????????", part, data[part]
                data[part] = common
            self.logger.debug("{}:".format(part))
            flg, self.pass_data, message = _play(piece_data_=pieces[part],
                                                                    data_=data[part],
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
            mod = importlib.import_module(hook_name)
            reload(mod)
            self.logger.debug("name        : {} ({})".format(piece_data["name"], hook_name))
            self.logger.debug("description : {}".format(piece_data["description"]))
            if hasattr(mod, "_PIECE_NAME_"):
                mod = getattr(mod, mod._PIECE_NAME_)(piece_data=piece_data,
                                                                                 data=data,
                                                                                 pass_data=pass_data,
                                                                                 logger=self.logger)
            else:
                return False, pass_data, header, detail
            inp = datetime.datetime.now()
            results = mod.execute()
            self.logger.debug("{}\n".format(datetime.datetime.now() - inp))
            return results

        except:
            self.logger.debug(traceback.format_exc())
            return False, pass_data, header, detail


def execute_command(app, **kwargs):
    def _get_script(script_):
        if script_ is None:
            script_ = os.path.dirname(__file__)
            script_ = "{}/PuzzleBoot.py".format(script_.replace("\\", "/"))
        else:
            script_ = script_.replace("/", "\\")

        return script_

    if "start_signal" in kwargs:
        kwargs["start_signal"].emit()

    script = _get_script(kwargs.get("script", None))
    if app.endswith("mayapy.exe"):
        cmd = r'"{}" "{}"'.format(app.replace("/", "\\"), script.replace("/", "\\"))

    elif app.endswith("mayabatch.exe") or app.endswith("maya.exe"):
        cmd = r'''"{}" -command "python(\\"execfile('{}')\\");"'''.format(app, script)

    elif app.endswith("motionbuilder.exe"):
        cmd = r'"{}" -suspendMessages -g 50 50 "{}"'.format(app.replace("/", "\\"), script.replace("/", "\\"))

    elif app.endswith("maya.exe"):
        sys_path = kwargs.get("sys_path", False)
        if not sys_path:
            return False
        sys_path = sys_path.replace("\\", "/")
        log_name = kwargs.get("log_name", "puzzle")

        cmd = '"{}" -command '.format(app)
        cmd += '"python(\\\"import sys;import os;sys.path.append(\\\\\\"{}\\\\\\");'.format(sys_path)
        cmd += 'from puzzle.Puzzle import Puzzle;x=Puzzle(\\\\\\"{}\\\\\\", '.format(log_name)
        cmd += 'file_mode=True, update_log_config=True)\\\");"'
    else:
        print "return: False"
        return False
    if kwargs.get("bat_file", False):
        bat = "SET __PUZZLE_FILE_MODE__=True\n"
        bat += "SET __PUZZLE_DATA_PATH__={}\n".format(str(kwargs["data_path"]))
        bat += "SET __ALL_PIECES_PATH__={}\n".format(str(kwargs["piece_path"]))
        bat += "SET __PUZZLE_LOGGER_NAME__={}\n".format(str(kwargs["log_name"]))
        bat += "SET __PUZZLE_LOGGER_DIRECTORY__={}\n".format(str(kwargs.get("log_directory", False)))
        bat += "SET __PIECES_KEYS__={}\n".format(str(kwargs["keys"]))
        bat += "SET __PUZZLE_APP__={}\n".format(str(app))
        bat += "SET __PUZZLE_PATH__={}\n".format(str(kwargs["sys_path"]))
        bat += "SET __PUZZLE_HOOKS__={}\n".format(str(kwargs["hook_path"]))
        bat += "SET __PUZZLE_MESSAGE_OUTPUT__={}\n".format(str(kwargs["message_output"]))
        bat += "SET __PUZZLE_CLOSE_APP__=True\n"
        if "standalone_python" in kwargs:
            bat += "SET __PUZZLE_STANDALONE_PYTHON__={}\n".format(str(kwargs["standalone_python"]))
        bat += cmd

        if not os.path.exists(os.path.dirname(kwargs["bat_file"])):
            os.makedirs(os.path.dirname(kwargs["bat_file"]))
        tx = open(kwargs["bat_file"], "w")
        tx.write(bat)
        tx.close()
        print "bat::oooooooooooooooo::", bat, kwargs.get("bat_start", False)
        if kwargs.get("bat_start", False):
            res = subprocess.Popen(kwargs["bat_file"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False).communicate()
            for r in res:
                print r

    else:
        env_copy = os.environ.copy()
        env_copy["__PUZZLE_FILE_MODE__"] = "True"
        env_copy["__PUZZLE_DATA_PATH__"] = str(kwargs["data_path"])
        env_copy["__ALL_PIECES_PATH__"] = str(kwargs["piece_path"])
        env_copy["__PUZZLE_LOGGER_NAME__"] = str(kwargs["log_name"])
        env_copy["__PUZZLE_LOGGER_DIRECTORY__"] = str(kwargs.get("log_directory", False))
        env_copy["__PIECES_KEYS__"] = str(kwargs["keys"])
        env_copy["__PUZZLE_APP__"] = str(app)
        env_copy["__PUZZLE_PATH__"] = str(kwargs["sys_path"])
        env_copy["__PUZZLE_HOOKS__"] = str(kwargs["hook_path"])
        env_copy["__PUZZLE_MESSAGE_OUTPUT__"] = str(kwargs["message_output"])
        env_copy["__PUZZLE_CLOSE_APP__"] = "True"
        if "standalone_python" in kwargs:
            env_copy["__PUZZLE_STANDALONE_PYTHON__"] = str(kwargs["standalone_python"])

        print ".......................", cmd, "#????????????????????????????????#"
        res = subprocess.Popen(cmd, env=env_copy, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False).communicate()
        for r in res:
            try:
                print r
            except:
                print("failed")


    if "end_signal" in kwargs:
        kwargs["end_signal"].emit(kwargs)

    return cmd

