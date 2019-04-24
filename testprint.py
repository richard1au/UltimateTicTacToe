from board import Board
import numpy as np

testBoard = Board(np.zeros((10,10), dtype = "int8"))
testBoard.place(2,2,1)
testBoard.print_board()
