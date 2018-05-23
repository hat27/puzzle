#-*- coding: utf8 -*-

import os
import sys
import unittest
import yaml
import json

module_path = os.path.normpath(os.path.join(__file__, "..\\..\\..\\"))
print module_path
if not module_path in sys.path:
  sys.path.append(module_path)

sys.dont_write_bytecode = True

from unittest import TestCase
from puzzle.Puzzle import Puzzle, execute_command


class TestPuzzle(TestCase):
    def setUp(self):
        data_directory = "{}/test/data".format(os.path.normpath(os.path.join(__file__, "..\\..\\")))
        data_path = "{}/data.json".format(data_directory)
        piece_yml = "{}/piece.yml".format(data_directory)

        self.data = json.load(open(data_path, "r"), "utf8")
        self.pieces = yaml.load(open(piece_yml))

    def test_normal_each(self):
        pz = Puzzle("sample", new=True, update_log_config=True)
        results = pz.play(self.pieces["data"]["sample01"], self.data["data"], {})
        for result in results:
            print(result)


class TestBatPuzzle(TestCase):
    def setUp(self):
        self.data_directory = "{}/test/data".format(os.path.normpath(os.path.join(__file__, "..\\..\\")))
        data_path = "{}/data.json".format(self.data_directory)
        piece_yml = "{}/piece.yml".format(self.data_directory)

        self.data = json.load(open(data_path, "r"), "utf8")
        self.pieces = yaml.load(open(piece_yml))

        self.dic = {}
        self.dic["data_path"] = data_path
        self.dic["piece_path"] = piece_yml
        self.dic["log_name"] = "test_sample"
        self.dic["log_directory"] = self.data_directory
        self.dic["keys"] = "sample01;close_app"
        self.dic["sys_path"] = module_path
        self.dic["hook_path"] = module_path
        self.dic["message_output"] = "{}/message_log.json".format(self.data_directory)

    def test_execute_from_prompt_win(self):
      """
      コマンドプロンプトからウィンドウズの処理を実行
      """
      app = "cmd.exe"
      self.dic["log_name"] = "test_execute_from_prompt_win"
      print(execute_command(app, **self.dic))

    def test_execute_from_prompt_maya(self):
      """
      コマンドプロンプトからmayaを起動して実行
      """
      self.dic["log_name"] = "test_execute_from_prompt_maya"
      app = "C:\\Program Files\\Autodesk\\Maya2018\\bin\\maya.exe"
      print(execute_command(app, **self.dic))

    def test_execute_from_prompt_mayapy(self):
      """
      コマンドプロンプトからmayapyを起動して実行
      """
      self.dic["log_name"] = "test_execute_from_prompt_mayapy"
      app = "C:\\Program Files\\Autodesk\\Maya2018\\bin\\mayapy.exe"
      print(execute_command(app, **self.dic))

    def test_execute_from_prompt_mayabatch(self):
      """
      コマンドプロンプトからmayabatchを起動して実行
      """
      self.dic["log_name"] = "test_execute_from_prompt_mayabatch"
      app = "C:\\Program Files\\Autodesk\\Maya2018\\bin\\mayabatch.exe"      
      print(execute_command(app, **self.dic))

    def test_execute_from_app_mayabatch(self):
      """
      mayaからmayabatchを起動して実行
      """
      self.dic["log_name"] = "test_execute_from_app_mayabatch"
      app = "C:\\Program Files\\Autodesk\\Maya2018\\bin\\mayabatch.exe"      
      print(execute_command(app, **self.dic))

    def test_execute_from_bat(self):
      """
      mayaからmayabatchを起動して実行
      """
      self.dic["log_name"] = "test_execute_from_bat"
      app = "C:\\Program Files\\Autodesk\\Maya2018\\bin\\mayabatch.exe"
      self.dic["bat_file"] = "{}/test.bat".format(self.data_directory)
      print(execute_command(app, **self.dic))


if __name__ == "__main__":
    unittest.main()