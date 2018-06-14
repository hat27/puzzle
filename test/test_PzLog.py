# -*- coding: utf8 -*-

import os
import sys
import time
import shutil
import unittest

module_path = os.path.normpath(os.path.join(__file__, "..\\..\\..\\"))
print module_path
if module_path not in sys.path:
    sys.path.append(module_path)

sys.dont_write_bytecode = True

from puzzle.PzLog import PzLog
import puzzle.pz_env as pz_env


class PzLogTest(unittest.TestCase):
    def test_create_log_directory(self):
        log = PzLog()
        log_path = "C:/Users/Hattori/AppData/Local/Temp/puzzle/log/unknown.log"
        config_path = "C:/Users/Hattori/AppData/Local/Temp/puzzle/log/config/unknown.conf"
        self.assertEqual(log.log_path, log_path)
        self.assertEqual(log.config_path, config_path)
        self.assertEqual(os.path.exists(log.log_path), True)
        self.assertEqual(os.path.exists(log.config_path), True)

        log = PzLog(name="log_test")
        log_path = "C:/Users/Hattori/AppData/Local/Temp/puzzle/log/log_test.log"
        config_path = "C:/Users/Hattori/AppData/Local/Temp/puzzle/log/config/log_test.conf"

        self.assertEqual(log.log_path, log_path)
        self.assertEqual(log.config_path, config_path)
        self.assertEqual(os.path.exists(log.log_path), True)
        self.assertEqual(os.path.exists(log.config_path), True)

        log_directory = "{}_".format(pz_env.get_log_directory())
        log = PzLog(name="log_test", log_directory=log_directory)
        log_path = "C:/Users/Hattori/AppData/Local/Temp/puzzle/log_/log_test.log"
        config_path = "C:/Users/Hattori/AppData/Local/Temp/puzzle/log_/config/log_test.conf"

        self.assertEqual(log.log_path, log_path)
        self.assertEqual(log.config_path, config_path)
        self.assertEqual(os.path.exists(log.log_path), True)
        self.assertEqual(os.path.exists(log.config_path), True)

    def test_use_default_config(self):
        template = "{:04d}_{:02d}_{:02d}_{:02d}_{:02d}"
        log = PzLog()
        time.sleep(60)
        file_meta = time.localtime(os.stat(log.config_path).st_mtime)
        mtime = template.format(*file_meta)

        log2 = PzLog()
        time.sleep(60)
        file_meta = time.localtime(os.stat(log2.config_path).st_mtime)
        mtime2 = template.format(*file_meta)
        result = mtime == mtime2
        self.assertEqual(result, True)

        time.sleep(60)
        log3 = PzLog(use_default_config=True)

        file_meta = time.localtime(os.stat(log3.config_path).st_mtime)
        mtime3 = template.format(*file_meta)
        result = mtime == mtime3
        print 333, mtime2
        self.assertEqual(result, False)

    def test_check_save_file_name(self):
        log = PzLog()
        exists = False
        with open(log.config_path, "r") as f:
            f_s = f.read().split("\n")
            for l in f_s:
                if log.log_path in l:
                    exists = True
                    break

        self.assertEqual(exists, True)

    def test_change_level(self):
        log = PzLog()

        tx = open(log.log_path, "r")
        result1 = len([l for l in tx.read().split("\n") if l != ""])
        log.logger.debug("debug")

        tx = open(log.log_path, "r")
        result2 = len([l for l in tx.read().split("\n") if l != ""])
        self.assertEqual(result1+1, result2)

        log.remove_handler()

        tmp = log.config_path.replace(".conf", "_.conf")
        shutil.copy2(log.config_path, tmp)
        with open(tmp, "r") as f:
            with open(log.config_path, "w") as new:
                f_s = f.read().split("\n")
                for l in f_s:
                    if "DEBUG" in l:
                        l = l.replace("DEBUG", "INFO")

                    new.write("{}\n".format(l))

        log = PzLog()
        log.logger.debug("debug")
        log.logger.debug("debug2")
        log.logger.debug("debug3")
        log.logger.info("info")

        tx = open(log.log_path, "r")
        result3 = len([l for l in tx.read().split("\n") if l != ""])
        self.assertEqual(result2+1, result3)


if __name__ == "__main__":
    unittest.main()