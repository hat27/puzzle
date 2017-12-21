#-*- coding: utf8 -*-

import os
import sys

import logging.config
from logging import getLogger

from . import pz_env

class Log(object):
    def __init__(self, name=None, remove=False, **args):
        if name is None:
            name = "unknown"

        self.name = name
        if remove:
            previous_logger = getLogger(self.name)
            for handler in previous_logger.handlers[::-1]:
                self.logger.removeHandler(handler)

        replace_log_config = args.get("replace_log_config", {})
        replace_log_config["$NAME"] = name
        path = self.get_log_config(replace_log_config, args.get("force", True))
        logging.config.fileConfig(path)
        self.logger = getLogger(self.name)
        self.logger.propagate = False

    def get_log_config(self, replace_log_config, force=True):
        def _replace(w, replace_log_config):
            for k, v in replace_log_config.items():
                if k in w:
                    return w.replace(k, v)
            return w

        path = "%s/config/%s.conf" % (pz_env.get_log_directory(), self.name)
        save_path = "%s/%s.log" % (pz_env.get_log_directory(), self.name)
        replace_log_config["$SAVEFILE"] = save_path
        template = pz_env.get_log_template()
        if os.path.exists(path):
            if not force:
                return path

        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        with open(template, "r") as tx:
            tx_s = tx.read().split("\n")
            tx = open(path, "w")
            new = [_replace(l, replace_log_config) for l in tx_s]
            tx.write("\n".join(new))
            tx.close()

        return path

if __name__ == "__main__":
    import sys
    sys.path.append("G:/works")
    x = Log("XXXXXX", remove=True, force=True)
    x.logger.debug("test")