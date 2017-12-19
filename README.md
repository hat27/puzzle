# "puzzle" is the most simplest job platform for python tools.  

## description
The objective of this module is to separate command from gui.  
  
## use  
"puzzle" needs couple of data.  
module setting data(calls "piece") and source data.  
we will write a lot of small "pieces" to solve the problem.  
  
"puzzle" has "normal mode" and "file mode".  
  
### normal mode
just do it on script
  
### file mode
just do it from file(s)  
this mode may usefull when we wants to do process outside of our tools (or app)  
  
## startup
1. open "__init__.py" and set **PUZZLE_MODULE_PATH** to environ  
2. open "test/normal_mode_test.py" and set **PUZZLE_MODULE_PATH** to environ   
3. run "test/test_normal_mode.py" or "test/test_file_mode.py"  
※much easier to set **PUZZLE_MODULE_PATH** to "environment variable"  
  
## prepare  
### 1. module setting data like(yml, json)  
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

     ``` 
    "primary": {  
                "open_path": "D:/project/c001/c001.ma"  
               }  
     ``` 
  
## sample module  
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
