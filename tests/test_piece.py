import unittest

from puzzle.Piece import Piece

class GetPieceValue(unittest.TestCase):
    def test_paint(self):
        piece_data = {
            "paint": {
                "a": "a_override_key",
                "b": "b_override_key"
            }
        }
        data = {
            "b_override_key": "aaaa"
        }

        piece = Piece(data=data, piece_data=piece_data)
        result = {"b": "aaaa"}
        self.assertEqual(piece.data, result)
    
    def test_filter(self):
        # if False, skip job
        piece_data = {
            "filters": [{"category": "CH"}]
        }

        data = {
            "category": "CH"
        }

        piece = Piece(data=data, piece_data=piece_data)
        self.assertEqual(piece.filtered, True)

        data = {
            "category": "BG"
        }

        piece = Piece(data=data, piece_data=piece_data)
        self.assertEqual(piece.filtered, False)
    
    def test_value_override(self):
        piece_data = {
            "paint": {
                "start": "@start"
            }
        }

        data = {
            "start": 0
        }

        pass_data = {
            "start": 101
            }

        piece = Piece(piece_data=piece_data, 
                      data=data, 
                      pass_data=pass_data)

        result = {"start": 101}
        self.assertEqual(piece.data, result)

import sys
print(sys.path)
if __name__ == "__main__":
    unittest.main()


