import numpy as np
import math
import operator
import time

infinity = 999999


class RandomPlacing():
    # actual depth = abpdepth + 1
    max = {}
    min = {}
    nearby = [-9, -8, -7, -1, 1, 7, 8, 9]

    def __init__(self, game, player):
        # Player will always be White(1/friend), as we pass in canonical board
        self.game = game
        self.player = player
        self.abpDepth = 4

    def timeOut(self):
        if abs(time.time() - self.time) > 2000:
            return True
        return False

    def search(self, board, turn, curPlayer):
        """
        input: A canonical board
        return: a action number in range(513)
        """

        valids = self.game.getValidMoves(board, curPlayer)

        a = np.random.randint(self.game.getActionSize())
        while valids[a] != 1:
            a = np.random.randint(self.game.getActionSize())
        return a



