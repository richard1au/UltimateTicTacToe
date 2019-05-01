#!/usr/bin/python3
# Sample starter bot by Zac Partrdige
# 06/04/19
# Feel free to use this and modify it however you wish

#Modified by Richard Lau and Matt Gelabert

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
curr = 0 # this is the current board to play in
global_nummoves = 0
global_depth = 5

# choose a move to play
#play should use new updated board, create a new game tree with it.
#first initialise root BoardNode
#pass Board node into game tree
#run alphabeta using gametree function
#game tree utilises nodes generatechildren() functions

def play():
    # boards.print_board()

    # just play a random move for now

    #How i plan to do it
    #n = alphaBetaSearch(chosen depth)
    #return n

    '''
    n = np.random.randint(1,9)
    while boards.get_tile(curr, n) != 0:
        n = np.random.randint(1,9)
    '''
    # print("playing", n)

    #Temporary fix for not making "winning moves". It gets close to winning moves but never
    #makes them...
    # for child in boards.generate_children():
    #     if child.won():
    #         return child.get_boardtoplayin()
    # n = alphaBetaSearch(4)
    #print(n)

    #Every 7 moves, increment depth of search by one
    global global_depth
    global global_nummoves

    n = alphaBetaSearch(global_depth)
    place(curr, n, 1)
    global_nummoves += 1
    if global_nummoves % 5 == 0:
        global_depth += 1
    print(f'Depth : {global_depth}, Num_Moves: {global_nummoves}')

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
    
    
def alphaBetaSearch(depth):
    alpha = [-99999, 0]
    beta = [99999, 0]
    maxalpha = alphaBetaHelper(boards, depth, alpha, beta)
    #print("////",maxalpha[0], " ", maxalpha[1],"////")
    return maxalpha[1]


def alphaBetaHelper(node, depth, alpha, beta):
    if node.is_terminal() or depth == 0:
        #print(node.compute_heuristic(1, 2))
        return [node.compute_heuristic(1, 2),  node.get_boardtoplayin()]

    if node.get_player() == 2:
        for child in node.generate_children():
            childAlpha = alphaBetaHelper(child, depth-1, alpha, beta)
            if(childAlpha[0] > alpha[0]):
                alpha = [childAlpha[0], child.get_boardtoplayin()]
            if alpha[0] >= beta[0]:
                return alpha
        return alpha

    else:
        for child in node.generate_children():
            childBeta = alphaBetaHelper(child, depth-1, alpha, beta)
            if(childBeta[0] < beta[0]):
                beta = [childBeta[0], child.get_boardtoplayin()]
            if alpha[0] >= beta[0]:
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
