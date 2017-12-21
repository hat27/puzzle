#-*- coding: utf8 -*-

import os
import sys


module_path = "somewhere" 
sys.path.append(module_path)

sys.dont_write_bytecode = True


from puzzle.Puzzle import Puzzle

pieces = {
          "primary": [
                      {
                       "name": "open",
                       "description": "open file",
                       "piece": "puzzle.pieces.test.open_file",
                       "paint": {
                                 "open_path": "maya_open_path"
                                }
                      }                          
                     ],
            "main": [
                      {
                       "name": "reference chara",
                       "description": "reference chara assets",
                       "piece": "puzzle.pieces.test.reference_chara",
                       "filters": [{"asset_type": "chara"}]
                      },
                      {
                       "name": "reference prop",
                       "description": "reference prop assets",
                       "piece": "puzzle.pieces.test.reference_prop",
                       "filters": [{"asset_type": "prop"}]
                      },
                      {
                       "name": "import fbx",
                       "description": "import fbx",
                       "piece": "puzzle.pieces.test.import_fbx",
                       "filters": [{"asset_type": ["chara", "prop"]}]
                      }                          
                    ],
            "post": [
                     {
                      "name": "save",
                      "description": "save file",
                      "piece": "puzzle.pieces.test.save_file",
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

x = Puzzle("sample", new=True, update_log_config=True)
results = x.play(pieces, data, {})
print
print
for result in results:
  print result



