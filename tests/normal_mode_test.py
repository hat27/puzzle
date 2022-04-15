#-*- coding: utf8 -*-

import os
import sys


module_path = os.path.normpath(os.path.join(__file__, "../../../"))
if not module_path in sys.path:
  sys.path.append(module_path)

sys.dont_write_bytecode = True


from puzzle.Puzzle import Puzzle, execute_command

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
                    ],

              "finally": [
                  {
                      "name": "end dialog",
                      "description": "run ui",
                      "piece": "puzzle.pieces.app.PzEndDialog.main"
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
os.environ["__PUZZLE_PATH__"] = module_path
x = Puzzle("sample", new=True, update_log_config=True)
results = x.play(pieces, data, {})
for result in results:
  print(result)

app = "C:/Program Files/Autodesk/Maya2015\\bin\\mayapy.exe".replace("/", "\\")

dic = {'piece_path': 'K:/staff/hattori/KbnToolBox/config/pipeline/env/PzPieces/_base_.yml',
       'sys_path': 'K:/staff/hattori/KbnToolBox/python/KbnLib/site-packages/Python27',
       'log_name': 'backburner_job',
       'log_directory': 'K:/staff/hattori/KbnToolBox/config/log/Hattori', 'keys': 'backburner_job',
       'data_path': '\\\\maestro\\staff\\hattori\\works\\daily\\20180517\\aaaxx02.json',
       'hook_path': 'K:/staff/hattori/KbnToolBox/python/KbnHooks',
       'message_output': 'K:/staff/hattori/KbnToolBox/config/log/Hattori/message_log.json'}

execute_command(app, **dic)
