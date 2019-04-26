from board import Board
import numpy as np

#Make test board, print state, then place, print state then commence testing
testBoard = Board(np.zeros((10,10), dtype = "int8"))
testBoard.print_board()
testBoard.place(1,2,2)
children = testBoard.generate_children()
for child in children:
    child.print_board()
