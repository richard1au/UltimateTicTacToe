import numpy as np

class Board:

    def __init__(self, state):
        self._state = state

    @property
    def state(self):
        return self._state

    def get_tile(self, board, num):
        return self._state[board][num]

    def place(self, board, num, player):
        self._state[board][num] = player

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
        print()
