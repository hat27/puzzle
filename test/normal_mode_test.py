#-*- coding: utf8 -*-

import os
import sys

os.environ.setdefault("PUZZLE_MODULE_PATH", "somewhere")
sys.path.append(os.environ["PUZZLE_MODULE_PATH"])

sys.dont_write_bytecode = True


import puzzle.env as env
from puzzle.Puzzle import Puzzle

print env.get_log_directory()

x = Puzzle("sample", log_force=True)
pieces = {
          "primary": [
                      {
                       "name": "open",
                       "description": "open file",
                       "piece": "puzzle.pieces.test.test01",
                       "paint": {
                                 "open_path": "maya_open_path"
                                }
                      }                          
                     ],
            "main": [
                      {
                       "name": "reference chara",
                       "description": "reference chara assets",
                       "piece": "puzzle.pieces.test.test02",
                       "filters": [{"asset_type": "chara"}]
                      },
                      {
                       "name": "reference prop",
                       "description": "reference prop assets",
                       "piece": "puzzle.pieces.test.test03",
                       "filters": [{"asset_type": "prop"}]
                      },
                      {
                       "name": "import fbx",
                       "description": "import fbx",
                       "piece": "puzzle.pieces.test.test04",
                       "filters": [{"asset_type": ["chara", "prop"]}]
                      }                          
                    ],
            "post": [
                     {
                      "name": "save",
                      "description": "save file",
                      "piece": "puzzle.pieces.test.test05",
                      "paint": {
                                "save_path": "maya_save_path"
                               }
                     }
                    ]
              }

data = {
        "primary": {
                    "maya_open_path": None
                   }, 

        "main": [
                 {
                  "asset_type": "chara",
                  "namespace": "A",
                  "asset_path": "D:/project/A.ma",
                  "fbx_path":  "D:/project/c001_A.fbx"
                 },
                 {
                  "asset_type": "prop",
                  "namespace": "B",
                  "asset_path": "D:/project/B.ma",
                  "fbx_path":  "D:/project/c001_B.fbx"
                 },
                 {
                  "asset_type": "BG",
                  "namespace": "BG",
                  "asset_path": "D:/project/BG.ma",
                  "fbx_path":  "D:/project/c001_BG.fbx"
                 },
                ],

        "post": {
                 "save_path": "D:/project/c001.ma"
                }

       }

results = x.play(pieces, data, {})
print
print
for result in results:
  print result



