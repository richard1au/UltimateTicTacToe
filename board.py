import numpy as np
from copy import copy

#Do note that this board class functions work heavily under the 
#assumption that a randomly made first move has been done in order to generate children!
class Board:

    def __init__(self, state):
        self._state = state
        self._boardplayedin = 0
        self._boardtoplayin = 0
        self._player = 0


    @property
    def state(self):
        return self._state

    #remember for agent.py heuristic is computed from player 2 point of view
    def compute_heuristic(self):
        return heuristicBoard(self)
    
    def get_tile(self, board, num):
        return self._state[board][num]

    def place(self, board, num, player):
        self._state[board][num] = player
        self._boardplayedin = board
        self._boardtoplayin = num
        self._player = player

    def print_board_row(self, a, b, c, i, j, k):
        # The marking script doesn't seem to like this either, so just take it out to submit
        print("", self._state[a][i], self._state[a][j], self._state[a][k], end = " | ")
        print(self._state[b][i], self._state[b][j], self._state[b][k], end = " | ")
        print(self._state[c][i], self._state[c][j], self._state[c][k])

    def print_board(self):
        self.print_board_row(1,2,3,1,2,3)
        self.print_board_row(1,2,3,4,5,6)
        self.print_board_row(1,2,3,7,8,9)
        print(" ------+-------+------")
        self.print_board_row(4,5,6,1,2,3)
        self.print_board_row(4,5,6,4,5,6)
        self.print_board_row(4,5,6,7,8,9)
        print(" ------+-------+------")
        self.print_board_row(7,8,9,1,2,3)
        self.print_board_row(7,8,9,4,5,6)
        self.print_board_row(7,8,9,7,8,9)
        #print()
        print("heuristic: ", self.compute_heuristic(), "\n")

    def is_terminal(self):
        return self.boardfull() or self.won()

    def boardfull(self):
        for i in range(1, 9):
            for j in range(1, 9):
                if self._state[i][j] == 0:
                    return False 

        return True

    def won(self):
        b = self._state[self._boardplayedin]
        p = self._player
        return (b[1]==b[2]==b[3]==p or
                b[4]==b[5]==b[6]==p or
                b[7]==b[8]==b[9]==p or
                b[1]==b[4]==b[7]==p or
                b[2]==b[5]==b[8]==p or
                b[3]==b[6]==b[9]==p or
                b[1]==b[5]==b[9]==p or
                b[3]==b[5]==b[7]==p)

    def generate_children(self):
        children = []
        b = self._state[self._boardplayedin]
        for i in range(1,10):
            if b[i] == 0:
                newBoard = Board(copy(self._state))
                newBoard.place(self._boardplayedin, i, self.next_player())
                children.append(newBoard)

        return children
        
    def get_player(self):
        return self._player

    def next_player(self):
        if self._player == 2:
            return 1
        return 2
        
 
        


# calculates the heuristic of the entire board
def heuristicBoard(self):
    total = 0
    for i in range(1,9):
        total += heuristicSmall(self, i)
    return total


# evaluates the heuristic for a 3x3 board
def heuristicSmall(self, i):
    totalX = 0
    totalO = 0
    currX = 0
    currO = 0    
    
    # calculates for each row 
    for k in range(1,10):
        if self.get_tile(i,k) == self._player:
            currX += 1
        if self.get_tile(i,k) == self.next_player():
            currO += 1
        if k % 3 == 0:
            totalX += heuristicAddX(currX, currO)
            totalO += heuristicAddO(currX, currO)
            currX = 0
            currO = 0
                
    #calculates for each column
    for k in range(0,3):
        for l in range(1,10,3):
            if self.get_tile(i,l+k) == self._player: 
                currX += 1
            if self.get_tile(i,l+k) == self.next_player(): 
                currO += 1      
        totalX += heuristicAddX(currX, currO)
        totalO += heuristicAddO(currX, currO)
        currX = 0
        currO = 0
                
    #calculates for each diagonal 
    for k in range(1,8,4):
        if self.get_tile(i,k) == self._player:
            currX += 1
        if self.get_tile(i,k) == self.next_player():
            currO += 1
    totalX += heuristicAddX(currX, currO)
    totalO += heuristicAddO(currX, currO)
    currX = 0
    currO = 0
        
    for k in range(3,8,2):
        if self.get_tile(i,k) == self._player:
            currX += 1
        if self.get_tile(i,k) == self.next_player():
            currO += 1
    totalX += heuristicAddX(currX, currO)
    totalO += heuristicAddO(currX, currO)
    currX = 0
    currO = 0
    
    return totalX-totalO


#helper function to find X score for a row/col/diagonal
def heuristicAddX(currX, currO):
    if currO == 0:
        if currX == 3:
            return 6
        if currX == 2:
            return 3
        if currX == 1:
            return 1
        else:
            return 0
    else:
        return 0
        
#helper function to find O score for a row/col/diagonal
def heuristicAddO(currX, currO):
    if currX == 0:
        if currO == 3:
            return 6
        if currO == 2:
            return 3
        if currO == 1:
            return 1
        else:
            return 0 
    else:
        return 0
                
