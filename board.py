import numpy as np
from copy import copy

#Board Class is a representation of a 9x9 tic tac toe board
class Board:
    #Contains storage of (9x9) numpy array along with various useful attributes of the current state of game
    def __init__(self, state, heurCurr = 0):
        self._state = state
        self._boardplayedin = 0
        self._boardtoplayin = 0
        self._player = 0
        self._heurCurr = heurCurr

    @property
    def state(self):
        return self._state
     
    def compute_heuristic(self, player1, player2):
        return self._heurCurr
    
    #Retrives either 0,1,2 at the specified board and position (num)
    def get_tile(self, board, num):
        return self._state[board][num]

    #Places player indiciator at specified board and position(num), updates attributes of board state
    def place(self, board, num, player):
        prevHeur = heuristicSmall(self, board, 1, 2)
        self._state[board][num] = player
        self._boardplayedin = board
        self._boardtoplayin = num
        self._player = player
        newHeur = heuristicSmall(self, board, 1, 2)
        self._heurCurr += newHeur - prevHeur
        
    #Determines if the board is in a finishing state (either full or won)
    def is_terminal(self):
        return self.boardfull() or self.won()

    #Board is full when there are no empty positions (0)
    def boardfull(self):
        for i in range(1, 9):
            for j in range(1, 9):
                if self._state[i][j] == 0:
                    return False 

        return True

    #Board is won where there is three in a row
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

    #Generates next possible game states to one depth in a list
    def generate_children(self):
        children = []
        b = self._state[self._boardtoplayin]  #Gets the board to be played in
        for i in range(1,10): 
            if b[i] == 0: #Checks all positions on board, if empty there is a valid move
                newBoard = Board(copy(self._state), self._heurCurr) #Create new Board object with copied state and current heuristic
                newBoard.place(self._boardtoplayin, i, self.next_player()) #Place new valid move
                children.append(newBoard)

        return children
        
    def get_player(self):
        return self._player

    #Tells us which player is to play after this board state
    def next_player(self):
        if self._player == 2:
            return 1
        return 2
        
    def get_boardtoplayin(self):
        return self._boardtoplayin
        
# evaluates the heuristic for a 3x3 board
def heuristicSmall(self, i, player1, player2):
    total1 = 0
    total2 = 0
    curr1 = 0
    curr2 = 0    
    
    # calculates for each row 
    for k in range(1,10):
        if self.get_tile(i,k) == player1:
            curr1 += 1
        if self.get_tile(i,k) == player2:
            curr2 += 1
        if k % 3 == 0: #Partitions totals for [(1, 2, 3), (4, 5, 6), (7, 8, 9)]
            total1 += heuristicAddX(curr1, curr2)
            total2 += heuristicAddO(curr1, curr2)
            curr1 = 0
            curr2 = 0
                
    #calculates for each column
    for k in range(0,3):
        for l in range(1,8,3):
            if self.get_tile(i,l+k) == player1: #l+k makes sure we are in the correct column. k iterating which column we look at
                curr1 += 1
            if self.get_tile(i,l+k) == player2: 
                curr2 += 1      
        total1 += heuristicAddX(curr1, curr2)
        total2 += heuristicAddO(curr1, curr2)
        curr1 = 0
        curr2 = 0
                
    #calculates for each diagonal 
    for k in range(1,10,4): #Positions (1, 5, 9)
        if self.get_tile(i,k) == player1:
            curr1 += 1
        if self.get_tile(i,k) == player2:
            curr2 += 1
    total1 += heuristicAddX(curr1, curr2)
    total2 += heuristicAddO(curr1, curr2)
    curr1 = 0
    curr2 = 0
        
    for k in range(3,8,2): #Positions (3, 5, 7)
        if self.get_tile(i,k) == player1:
            curr1 += 1
        if self.get_tile(i,k) == player2:
            curr2 += 1
    total1 += heuristicAddX(curr1, curr2)
    total2 += heuristicAddO(curr1, curr2)
    curr1 = 0
    curr2 = 0
    
    return total1 - total2 #total player 1 - total player 2 gives us a zero sum game.


#helper function to find player 1 (us) score for a row/col/diagonal
def heuristicAddX(curr1, curr2):
    if curr2 == 0:
        if curr1 == 3: #10,000 points for three in a row
            return 10000
        if curr1 == 2: #20 points for two in a row
            return 20
        if curr1 == 1: #1 point for just one piece
            return 1
        else:
            return 0
    else:
        return 0
        
#helper function to find player 2 (enemy) score for a row/col/diagonal
def heuristicAddO(curr1, curr2):
    if curr1 == 0:
        if curr2 == 3: #10,000 points for three in a row
            return 10000 
        if curr2 == 2: #20 points for two in a row
            return 20
        if curr2 == 1: #1 point for just one piece
            return 1
        else:
            return 0 
    else:
        return 0
                
