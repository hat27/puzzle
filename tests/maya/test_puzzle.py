import os
import sys
import unittest
import pprint
pprint.pprint(os.environ)
print("--------------------------------")
print(__file__)
print(os.listdir(__file__))
print("--------------------------------")
module_path = os.environ.get("PUZZLE_REPO_PATH")
if module_path:
    sys.path.append(module_path)
    sys.path.append(os.path.normpath(os.path.join(module_path, "../tests/data")))

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
          ]
        }

    def test_normal_each(self):
      puzzle = Puzzle()
      data = {
        "primary": {
          "start": 0, 
          "end": 10
          }
        }
      results = puzzle.play(self.pieces, data, pass_data={})
      self.assertEqual(results[0][0], True)

if __name__ == "__main__":
    unittest.main()