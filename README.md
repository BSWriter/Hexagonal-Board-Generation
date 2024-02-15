# Hexagonal-Board-Generation
## Installs
This code primarily uses the pygame library, so installs aren't necessary. Aside from that the math, sys, json, and random libraries are used, so make sure your installed version of python includes them.
## Scripts
### BoardGenerator
Main Script. Will prompt user to input board name (how the board is saved), the number of rows and columns, the size of the panels, and if the board should be surrounded by wall tiles.
### GenClasses
Class Script. Contains object code for tiles and board. Most likely, will not need to be modified for optimization.
## Notes
- When saving board, you will need to specify save path of json file on line 72 of BoardGenerator.py
