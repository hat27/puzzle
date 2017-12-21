#-*- coding: utf8 -*-

import os
import sys

import logging.config
from logging import getLogger

from . import env as pz_env

class Log(object):
    def __init__(self, name=None, new=False, **args):
        print name
        if name is None:
            name = "unknown"

        self.name = name
        if new:
            previous_logger = getLogger(self.name)
            for handler in previous_logger.handlers[::-1]:
                try:
                    self.logger.removeHandler(handler)
                except:
                    pass

        replace_log_config = args.get("replace_log_config", {})
        replace_log_config["$NAME"] = name
        path = self.get_log_config(replace_log_config, args.get("update_config", True))
        logging.config.fileConfig(path)
        self.logger = getLogger(self.name)
        self.logger.propagate = False

    def get_log_config(self, replace_log_config, update_config=True):
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
            if not update_config:
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
    x = Log("XXXXXX", new=True, update_config=True)
    x.logger.debug("test")