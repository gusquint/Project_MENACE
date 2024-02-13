# MENACE
[Video Demo](https://youtu.be/l1m1WZ4pIjg)
## Description:
This program plays Tic Tac Toe for itself and learns with every game according to this [document](https://www.mscroggs.co.uk/blog/19) I found on the internet.

Each game proceeds as follows. When it is the learning machine's turn, it analyzes the current board and searches its memory to see if that board has been played in the past. If not, it generates a dictionary with the possibilities for that board and another one with frequency weights for those possibilities. Then, it chooses one of those possibilities randomly. If the machine wins or ties, it increases the weights of the dictionary with the options it chose. If it loses, it reduces these weights. This makes the learning machine more likely to choose winning moves and less likely to choose losing moves. In the turn of the random machine (it does not learn), a possibility is chosen at random.

To prevent the memory of the learning machine from being lost, after the iterations selected by the user, the program saves the values ​​of both dictionaries in .csv files to be analyzed or used in this same program.


It is necessary to import the following:
```
from random import choice
from random import choices
import csv
```
## Functions:
Brief description with examples of the functions of the program
### Board methods:
### __init __
```
board=Board(["1","2","3","4","5","6","7","8","9"])
```
sets the `self.list` values to the list `["1","2","3","4","5","6","7","8","9"]` .  An argument of lenght other than 9 will raise `ValueError`.
```
board=Board()
```
The default value is `[" "," "," "," "," "," "," "," "," "]`

### __str __

When using the `print` function on a Board object, prints the values of `self.list` in the regular Tic Tac Toe shape.
```
>>>board=Board(["1","2","3","4","5","6","7","8","9"])
>>>print(board)
      1 | 2 | 3
     -----------
      4 | 5 | 6
     -----------
      7 | 8 | 9
```
### board.update (info)
Sets the values of `self.list` to those of `info`.  Will raise ``ValueError`` if `info` is not of lenght 9.  Will raise `TypeError` if `info` is not a string or list
```
>>>board.update(["1","2","3","4","5","6","7","8","9"])
>>>print(board)

      1 | 2 | 3
     -----------
      4 | 5 | 6
     -----------
      7 | 8 | 9

>>>board.update("123456789")
>>>print(board)

      1 | 2 | 3
     -----------
      4 | 5 | 6
     -----------
      7 | 8 | 9
```

### board.win ()
Returns `True` if the current board has 3 in line either horizontally, vertically or diagonally
```
>>>board.update("111456789")
>>>board.win()
True
```

### board.reset ()
Sets the current values of `self.list` to `[" "," "," "," "," "," "," "," "," "]`
```
>>>board.reset()
>>>print(board)
        |   |
     -----------
        |   |
     -----------
        |   |
```

### board.rotate_90 ()
Rotates the values of a board 90 degrees clockwise and updates the values of `self.list`
```
>>>print(board)

      1 | 2 | 3
     -----------
      4 | 5 | 6
     -----------
      7 | 8 | 9

>>>board.rotate_90()
>>>print(board)

      7 | 4 | 1
     -----------
      8 | 5 | 2
     -----------
      9 | 6 | 3
```

### board.flip_h ()
Flips the values of a board horizontally and updates the values of `self.list`
```
>>>print(board)

      1 | 2 | 3
     -----------
      4 | 5 | 6
     -----------
      7 | 8 | 9

>>>board.flip_h()
>>>print(board)

      3 | 2 | 1
     -----------
      6 | 5 | 4
     -----------
      9 | 8 | 7
```
### board.copy ()
Returns a copy of the current board.
```
>>>print(board)

      1 | 2 | 3
     -----------
      4 | 5 | 6
     -----------
      7 | 8 | 9

>>>newboard=board.copy()
>>>print(newboard)

      1 | 2 | 3
     -----------
      4 | 5 | 6
     -----------
      7 | 8 | 9
```

### board.string ()
Returns a string of values in `self.list`
```
>>>print(board)

      1 | 2 | 3
     -----------
      4 | 5 | 6
     -----------
      7 | 8 | 9

>>>string=board.string()
>>>print(string)

123456789
```

### Program Functions:
### get_options_dic (file)
Returns a dictionary with the values in `file`.  The file needs to be in ``.csv`` format where the rows are organized as follows:
The first cell is the board to analyze and the next cells contains the options to play.  All these values are strings.
Here is an example
```
         ,X        , X       ,  X      ,   X     ,    X    ,     X   ,      X  ,       X ,        X
    O X  ,X   O X  , X  O X  ,  X O X  ,   XO X  ,    OXX  ,    O XX ,    O X X
  OXO X  ,X OXO X  , XOXO X  ,  OXOXX  ,  OXO XX ,  OXO X X
OXOXO X  ,OXOXOXX  ,OXOXO XX ,OXOXO X X
OXOXOXXO ,OXOXOXXOX
```
The first string in every row are the keys of the dictionary.  The others are the values.
To avoid mistakes, is better to leave the creation of such file to the function `save_dic`.

``get_options_dic`` intentionally passes `IndexError` and `FileNotFoundError` to make a user friendly experience
```
>>>options=get_options_dic("test_file.csv")
>>>print(options)
{'         ': ['X        ', ' X       ', '  X      ', '   X     ', '    X    ', '     X   ', '      X  ', '       X ', '        X'], '    O X  ': ['X   O X  ', ' X  O X  ', '  X O X  ', '   XO X  ', '    OXX  ', '    O XX ', '    O X X'], '  OXO X  ': ['X OXO X  ', ' XOXO X  ', '  OXOXX  ', '  OXO XX ', '  OXO X X'], 'OXOXO X  ': ['OXOXOXX  ', 'OXOXO XX ', 'OXOXO X X'], 'OXOXOXXO ': ['OXOXOXXOX']}
```

### get_weights_dic (file)
Returns a dictionary with the values in `file`.  The file needs to be in ``.csv`` format where the rows are organized as follows:
The first cell is the board to analyze and the next cells contains the frequencies of the options to play.  All this values are strings.
Here is an example
```
         ,9,41,27,24,11,25,38,30,26
    O X  ,5,5,9,5,5,6,6
  OXO X  ,6,10,6,6,6
OXOXO X  ,7,6,6
OXOXOXXO ,10
```
The first string in every row are the keys of the dictionary.  The others are the values.
To avoid mistakes, is better to leave the creation of such file to the function `save_dic`.

``get_weights_dic`` intentionally passes `IndexError` and `FileNotFoundError` to make a user friendly experience
```
>>>weights=get_weights_dic("test_file.csv")
>>>print(weights)
{'         ': [9, 41, 27, 24, 11, 25, 38, 30, 26], '    O X  ': [5, 5, 9, 5, 5, 6, 6], '  OXO X  ': [6, 10, 6, 6, 6], 'OXOXO X  ': [7, 6, 6], 'OXOXOXXO ': [10]}
```

### save_dic (dictionary,file)
Creates a `.csv` file with the information in `dictionary` which needs to be a dictionary.
Every row in the file will be created as follows:
The key of the dictionary will be the first cell of the row.  The Values of the dictionary will be separated and each written in the subsequent cells of the row

### list_to_str (list:list)
Returns a string which consists of the values of the argument which needs to be a list
```
>>>string=list_to_str(["1","2","3","4","5","6","7","8","9"])
>>>print(string)

123456789
```

### game (options,weights,opponent,repetitions=1)
This is the Tic Tac Toe game.  `options` and `weights` are dictionaries.  The parameter `opponent` receives two posible values `"human"` and `"machine"`.
- `opponent = "human"` makes this a game against the machine and sets `repetitions` to one.
- `opponent = "machine"` makes this a game between machines where one learns and the other plays at random

The parameter `repetitions` needs to be an integer and refers to the amount of games of Tic Tac Toe to be played

### main ()
This puts it all together.  Prompts the user to select a choice between the following options:
1. Machine self learn.  If this option is selected, the user is then prompted to determine the amount of iterations to play.  After said iterations, the program creates two `.csv` files with the information acquired.  This is the machine's memory.
2. Play against the Machine.  Play one game against the learning machine.  After this game, the program creates two `.csv` files with the information acquired.
3. Leave the program.