"puzzle" is the most simplest job platform for python tools.  

use  
1. open "__init__.py" and set PUZZLE_MODULE_PATH to environ  
2. open "test/normal_mode_test.py" and set PUZZLE_MODULE_PATH to environ   
3. run "test/test_normal_mode.py" or "test/test_file_mode.py"  
※much easier to set to "environment variable"  


prepare  
1. module set like  
    "primary": [
                {  
                "name": "test",  
                "piece": "pieces.test.test01", # module path  
                "description": "" # for log  
                }
                ]  

2. data set like  
    "primary": {  
                "open_path": "D:/project/c001/c001.ma"  
               }  

module  
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
            return True, self.pass_data, message # simple message for user


thank you.

Gou Hattori
hatbot27@gmail.com
