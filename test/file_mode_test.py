#-*- coding: utf8 -*-

import os
import sys

os.environ.setdefault("PUZZLE_MODULE_PATH", "somewhere")
sys.path.append(os.environ["PUZZLE_MODULE_PATH"])

sys.dont_write_bytecode = True

import puzzle.env as env
from puzzle.Puzzle import Puzzle

x = Puzzle("sample", log_force=True)

all_pieces = {
             "test_piece":{
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
                                     "filters": [{"asset_type": ["chara", "prop"]}, {"name": "hoge"}]
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
                  "fbx_path":  "D:/project/c001_A.fbx",
                  "name": "hoge"
                 },
                 {
                  "asset_type": "prop",
                  "namespace": "B",
                  "asset_path": "D:/project/B.ma",
                  "fbx_path":  "D:/project/c001_B.fbx",
                  "name": "hoge"

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

root = env.get_temp_directory("sample")
import json
json.dump({"data": data, "info": {}}, open("%s/data.json" % root, "w"), "utf8", indent=4)
json.dump({"data": all_pieces, "info": {}}, open("%s/all_pieces.json" % root, "w"), "utf8", indent=4)
os.environ["__PUZZLE_FILE_MODE__"] = "True"
os.environ["__ALL_PIECES_PATH__"] = "%s/all_pieces.json" % root
os.environ["__PUZZLE_DATA_PATH__"] = "%s/data.json" % root
os.environ["__PIECES_KEYS__"] = "test_piece"

x = Puzzle("log_to_temp_path")
results = x.play_as_file_mode()

for result in results:
  print result

