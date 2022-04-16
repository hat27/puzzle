![Tests](https://github.com/hat27/puzzle/actions/workflows/test.yml/badge.svg)

# "puzzle" is the most simplest job framework for python tools.  
もっともシンプルなpythonジョブフレームワーク

## description
The objective of this module is to separate command from gui.  
  
このツールの目的はGUIとコマンドを分離するところにあります。  
分離したコマンドはコマンドラインで簡単実行することができます。

## language
python 2.7

## use  
"puzzle" needs couple of data.  
module setting data(calls "piece". py file) and source data(dict).  
we will write a lot of small "pieces" to solve the problem.  
  
"puzzle" has "normal mode" and "file mode".  
  
"puzzle"は2つのデータが必要です  
一つは処理が書かれているモジュール(.pyファイル。ピースと呼んでいます)  
もう一つは処理に必要な入力データです(dict形式)  
小さなピースをたくさん作って問題を解決しましょう  

### normal mode
just do it on script(run "play")  
  
スクリプトの中でplay関数を実行してください。  

### file mode
just do it from file(s)  
this mode may usefull when we wants to do process outside of our tools (or app)  
set environ and run "play_as_file_mode"

environ  
__PUZZLE_FILE_MODE__ = "True"  
__ALL_PIECES_PATH__ = pieces file(.yml or .json)  
__PUZZLE_DATA_PATH__ = data file(.json)  
__PIECES_KEYS__ = piece key(group of piece)  
  
  
外部プロセスとして実行する場合は環境変数に値を設定した状態で  
play_as_file_mode関数を実行してください  
  
環境変数  
__PUZZLE_FILE_MODE__ = "True"  
__ALL_PIECES_PATH__ = 設定ファイル(.yml or .json)  
__PUZZLE_DATA_PATH__ データファイル(.json)  
__PIECES_KEYS__ = 実行キー(処理の塊)  
  
## startup
run "test/test_normal_mode.py" or "test/test_file_mode.py" with python27
  
## prepare  
使い方  
  
### 1. module setting data like(yml, json)  
1. 設定ファイルを作成します。(pieces)  
   ```
    primary:  
        - name: open file  
          piece: pieces.maya.file_open  
          description: "open file for do some job" # for log   
   ``` 
    or
   ``` 
    "primary": [  
        {  
            "name": "open file",  
            "piece": "pieces.maya.file_open", # module path  
            "description": "open file for do some job" # for log  
        }  
    ]  
   ```    
  
### 2. input data like  
2. 入力するデータを用意します(data)  
     ``` 
    "primary": {  
                "open_path": "D:/project/c001/c001.ma"  
               }  
     ``` 

### 3. 実行します  
     ```
     puzzle.play(pieces, data)
    
     ```

## sample piece(module)  
(look "pieces/test" directory)  

    #-*- coding: utf8 -*-
    import os

    from puzzle.Piece import Piece

    _PIECE_NAME_ = "Test01"

    class Test01(Piece):
        def __init__(self, **args):
            super(Test01, self).__init__(**args)
            self.name = _PIECE_NAME_ 

        def execute(self):
            return True, self.pass_data, message
  
## licence  
MIT licence  
  
## author  
Gou Hattori  
hatbot27@gmail.com  
