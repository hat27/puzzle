import os
import sys
import unittest

import maya.standalone
maya.standalone.initialize()

import maya.cmds as cmds

MODULE_PATH = os.environ.get("PUZZLE_REPO_PATH")
if MODULE_PATH:
    sys.path.append(MODULE_PATH)

PIECES_PATH = os.environ.get("PUZZLE_PIECE_PATH")
if not PIECES_PATH and MODULE_PATH:
    PIECES_PATH = os.path.normpath(os.path.join(MODULE_PATH, "../tests/data"))

from unittest import TestCase
from puzzle.Puzzle import Puzzle, execute_command
from puzzle.Piece import Piece

class TestSimple(TestCase):
    def setUp(self):
        self.pieces = {
          "primary": [
            {
              "name": "new file",
              "piece": "piece.maya.file_new"
            }
          ],
          "main": [
            {
              "name": "create sphere",
              "piece": "piece.maya.create_sphere"
            }
          ]
        }

    def test_normal_each(self):
      if PIECES_PATH:
        puzzle = Puzzle(pieces_directory=PIECES_PATH)
      else:
        puzzle = Puzzle()
      data = {
        "primary": {
          "start": 0, 
          "end": 10
          }, 
         "main": [{
           "name": "a",
           "move": (10, 0, 0)
         },
         {
           "name": "b",
           "move": (0, 10, 0)
         },
         {
           "name": "c",
           "move": (0, 0, 10)
         }         
         ]
        }
      results = puzzle.play(self.pieces, data, pass_data={})

      self.assertEqual(cmds.objExists("a"), True)
      self.assertEqual(cmds.objExists("b"), True)
      self.assertEqual(cmds.objExists("c"), True)
      
      self.assertEqual(cmds.getAttr("a.tx"), 10)
      self.assertEqual(cmds.getAttr("b.ty"), 10)
      self.assertEqual(cmds.getAttr("c.tz"), 10)

class TestLoggerLevel(TestCase):
    def setUp(self):
        self.pieces = {
          "primary": [
            {
              "name": "new file",
              "piece": "piece.maya.file_new"
            }
          ],
          "main": [
            {
              "name": "create sphere",
              "piece": "piece.maya.create_sphere"
            }
          ]
        }

    def test_normal_each(self):
      if PIECES_PATH:
        puzzle = Puzzle(pieces_directory=PIECES_PATH, logger_level="info")
      else:
        puzzle = Puzzle()
      data = {
        "primary": {
          "start": 0, 
          "end": 10
          }, 
         "main": [{
           "name": "a",
           "move": (10, 0, 0)
         },
         {
           "name": "b",
           "move": (0, 10, 0)
         },
         {
           "name": "c",
           "move": (0, 0, 10)
         }         
         ]
        }
      results = puzzle.play(self.pieces, data, pass_data={})

      self.assertEqual(cmds.objExists("a"), True)
      self.assertEqual(cmds.objExists("b"), True)
      self.assertEqual(cmds.objExists("c"), True)
      
      self.assertEqual(cmds.getAttr("a.tx"), 10)
      self.assertEqual(cmds.getAttr("b.ty"), 10)
      self.assertEqual(cmds.getAttr("c.tz"), 10)

if __name__ == "__main__":
    unittest.main()