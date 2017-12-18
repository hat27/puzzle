#-*- coding: utf8 -*-

import os

_TEMP_PATH_ = os.environ["TEMP"].split(";")[0].replace("\\", "/")
_PLATFORM_ = False
try:
    import maya.cmds
    _PLATFORM_ = "maya"
except:
    pass

try:
    from pyfbsdk import FBSystem
    _PLATFORM_ = "mobu"
except:
    pass

if not _PLATFORM_:
    _PLATFORM_ = "win"

def get_log_template():
    return "%s/puzzle/log.template" % os.environ["PUZZLE_MODULE_PATH"]

def get_temp_directory(relative=""):
    path = "%s/puzzle/%s" % (_TEMP_PATH_, relative)
    if not os.path.exists(path):
        os.makedirs(path)
    if path.endswith("/"):
        path = path[:-1]
    return path

def get_log_directory():
    return get_temp_directory("log")

def get_user_name():
    if "PUZZLE_USERNAME" in os.environ:
        return os.environ["PUZZLE_USERNAME"]
    return os.environ["USERNAME"]

def get_platform():
    return _PLATFORM_

if __name__ == "__main__":
    os.environ["PUZZLE_MODULE_PATH"] = "G:/works"
    print get_log_template()
    print get_temp_directory()
    print get_temp_directory("temp/test")
    print get_log_directory()
    print get_user_name()
    print get_platform()