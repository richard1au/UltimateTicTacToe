#!/usr/bin/python3
# Sample starter bot by Zac Partrdige
# 06/04/19
# Feel free to use this and modify it however you wish

#Modified by Richard Lau and Matt Gelabert |Finalised 1/05/19|

#Answer to assignment question (How it works?, Algos/DS and Design Decisions)
#
# How it works general overview: 
# Anytime server gives input (i.e second_move, next move) parse() is called to determine what to do.
# For any move() required, it involves placement of moves made by enemy or random move of server and then
# Calling play() to determine the moves for us. Play simply calls alpha-beta search to determine us the next best move.
# Our alpha-beta search will generate child states recursively using the object methods of the global Board instance (which manages the state and behaviours of a Board).
# The move with maximum alpha is passed back along with the alpha in a array with it as a pair. The move retrived at parent node of the game tree (the global Board instance) will be returned.
# Play() retrieves the move and places it in our own board and then passes it back to the server

#Algorithms
# Main algorithm utilised in this assignment was traditional alpha-beta search on a minimax tree of limited depth.
# We mainly decided on this because we found it unfeasible to generate all possible states to maximum depth given the branching factor of 9 and 81 possible move depth
# Clearly we had to implement it in a better way and so we turned to this algorithm because it was straightforward to implement and ended up producing reasonable results.
# As long as lookt was of same or lower depth, this algorithm performed ok.
# MCTS had been observed to do quite poorly in this assignment because of the limited simulations you could do.

#Data Structure Choices
#Main DS choice was using a Board class. We found it useful to have a board class because it was easy to wrap and manage all functionalities relating to the board.
# This is in contrast to having the board and the methods relating to it hanging out. 
# Of course we weighed up the cost/benefit of not having object instances everywhere vs ease of use
#We utilised a numpy 10x10 structure simply because it is much more optimised than traditional arrays.

#Important Design Decisions
#We ITERATIVELY UPDATE the heuristics of each board. Since each board is generated per one move, and only one board in 9 is affected we can simply compute the change
#In heuristic for that board only and update the currheuristic. This means we do not have to compute all 9 boards for every leaf node. This is actually significantly more efficient
#If you do the math. i.e For 9 depth and 9 branching, the heurist cost is 9(boards) * 9^9 wheras we could do one board per node in the tree for 9^9 + 9^8 + .....
#We did this after a suggestion in the openlearning forums from a very helpful user Yifan, and it did improve our computation times.

#We also iteratively increase searching depth (via log function so we can increase quickly and then level out). 
#This is quite important because in early stages branching factor is very high, making high depth unfeasible.
#However in later stages branching factor is lower allowing us to achieve higher depth in search. You can also argue searching far ahead becomes much more important in late
#Game where moves have larger impacts. We still have trouble reaching very high depths +10 so we decided to starting leveling out the search close to that point.

#It is important to note that during recursive generation of children we create SHALLOW copies of the state and new Board instances. 
#We did attempt to implement it without having to copy and just use one instance of Board however we found virtually no improvement to our overhead costs and thus
#little gain in computational speed.

#Python so slow so sad :(

import socket
import sys
import numpy as np
from board import Board
import math

# a board cell can hold:
#   0 - Empty
#   1 - I played here
#   2 - They played here

boards = Board(np.zeros((10, 10), dtype="int8")) #10x10 because indexes 0 are not used
curr = 0 # this is the current board to play in
global_nummoves = 0 #number of moves made by us so far
global_depth = 3 #starting depth of search

#decide where and how to make our move
def play():

    #Simply to use global variables in python
    global global_depth 
    global global_nummoves

    n = alphaBetaSearch(global_depth) #alpha beta search to global_depth
    place(curr, n, 1) #place returned move

    global_nummoves += 1 #Num moves we have made (not including random) increases by one
    global_depth = max(global_depth, math.floor(math.log(global_nummoves, 1.58))+1) #Depth we will search next will be the max of current depth vs log function floor 

    return n

# place a move in the global boards
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
    
#Parent alpha beta search function which begins recursive call of alphabetahelper     
def alphaBetaSearch(depth):
    alpha = [-99999, 0] #alpha = [alphavalue (-inf), maximising move (0)]
    beta = [99999, 0] #beta = [betavalue (+inf), minimising move (0)]
    maxalpha = alphaBetaHelper(boards, depth, alpha, beta)
    return maxalpha[1] #return maximising move

#Recursive helper function which recursively generates children from global board and its children
#Runs traditional alpha beta search from tutorial learning activities
#Important to note we return tuples of [alpha/betavalue, movetogetvalue]
def alphaBetaHelper(node, depth, alpha, beta):
    if node.is_terminal() or depth == 0:
        return [node.compute_heuristic(),  node.get_boardtoplayin()]

    if node.get_player() == 2: #If player who just moved is enemy(2), then it is our turn (1)
        for child in node.generate_children():
            childAlpha = alphaBetaHelper(child, depth-1, alpha, beta)
            if(childAlpha[0] > alpha[0]): #Grabs maximum alpha
                alpha = [childAlpha[0], child.get_boardtoplayin()]
            if alpha[0] >= beta[0]: #Pruning
                return alpha
        return alpha

    else:
        for child in node.generate_children():
            childBeta = alphaBetaHelper(child, depth-1, alpha, beta)
            if(childBeta[0] < beta[0]): #Grabs minimum beta
                beta = [childBeta[0], child.get_boardtoplayin()]
            if alpha[0] >= beta[0]: #Pruning
                return beta
        return beta


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

if __name__ == "__main__":
    main()
