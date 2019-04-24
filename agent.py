#!/usr/bin/python3
# Sample starter bot by Zac Partrdige
# 06/04/19
# Feel free to use this and modify it however you wish

import socket
import sys
import numpy as np
from board import Board

# a board cell can hold:
#   0 - Empty
#   1 - I played here
#   2 - They played here

# the boards are of size 10 because index 0 isn't used
boards = Board(np.zeros((10, 10), dtype="int8"))
boards.place(2,2,1)
boards.place(2,3,1)
curr = 0 # this is the current board to play in


# choose a move to play
def play():
    # boards.print_board()

    # just play a random move for now
    n = np.random.randint(1,9)
    while boards.get_tile(curr, n) != 0:
        n = np.random.randint(1,9)

    # print("playing", n)
    place(curr, n, 1)
    return n

# place a move in the global boards
#Global curr is an issue, can't be bothered to fix this right now
def place(board, num, player):
    global curr
    curr = num
    boards.place(board, num, player)

# read what the server sent us and
# only parses the strings that are necessary
def parse(string):
    if "(" in string:
        command, args = string.split("(")
        args = args.split(")")[0]
        args = args.split(",")
    else:
        command, args = string, []

    if command == "second_move":
        place(int(args[0]), int(args[1]), 2)
        return play()
    elif command == "third_move":
        # place the move that was generated for us
        place(int(args[0]), int(args[1]), 1)
        # place their last move
        place(curr, int(args[2]), 2)
        return play()
    elif command == "next_move":
        place(curr, int(args[0]), 2)
        return play()
    elif command == "win":
        print("Yay!! We win!! :)")
        return -1
    elif command == "loss":
        print("We lost :(")
        return -1
    return 0

# connect to socket
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[2]) # Usage: ./agent.py -p (port)

    s.connect(('localhost', port))
    while True:
        text = s.recv(1024).decode()
        if not text:
            continue
        for line in text.split("\n"):
            response = parse(line)
            if response == -1:
                s.close()
                return
            elif response > 0:
                s.sendall((str(response) + "\n").encode())



# calculates the heuristic of the entire board
def heuristicBoard(boards):
    total = 0
    for i in range(1,9):
        total += heuristicSmall(boards, i)
    return total


# evaluates the heuristic for a 3x3 board
def heuristicSmall(boards, i):
    totalX = 0
    totalO = 0
    currX = 0
    currO = 0    
    
    # calculates for each row 
    for k in range(1,10):
        if boards.get_tile(i,k) == 1:
            currX += 1
        if boards.get_tile(i,k) == 2:
            currO += 1
        if k % 3 == 0:
            totalX += heuristicAddX(currX, currO)
            totalO += heuristicAddO(currX, currO)
            currX = 0
            currO = 0
                
    #calculates for each column
    for k in range(0,3):
        for l in range(1,10,3):
            if boards.get_tile(i,l+k) == 1: 
                currX += 1
            if boards.get_tile(i,l+k) == 2: 
                currO += 1
        totalX += heuristicAddX(currX, currO)
        totalO += heuristicAddO(currX, currO)
        currX = 0
        currO = 0
                
    #calculates for each diagonal 
    for k in range(1,10,3):
        if boards.get_tile(i,k) == 1:
            currX += 1
        if boards.get_tile(i,k) == 2:
            currO += 1
    totalX += heuristicAddX(currX, currO)
    totalO += heuristicAddO(currX, currO)
    currX = 0
    currO = 0
        
    for k in range(3,8,2):
        if boards.get_tile(i,k) == 1:
            currX += 1
        if boards.get_tile(i,k) == 2:
            currO += 1
    totalX += heuristicAddX(currX, currO)
    totalO += heuristicAddO(currX, currO)
    currX = 0
    currO = 0
    
    return totalX-totalO
    
    #print("totalX: ", totalX, "\ntotalO: ", totalO)


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


if __name__ == "__main__":
    print(heuristicBoard(boards))
    

