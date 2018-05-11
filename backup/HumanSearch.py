import numpy as np
import math
import operator
import time

infinity = 999999

FRIEND = 1
ENEMY = -1
EMPTY = 0


class HumanSearch():
    """
    NOTE:
    in this module, all things based on canonical board,
    and use coordinate (column, row)
    """

    def __init__(self, game, player):
        # Player will always be White(1/friend), as we pass in canonical board
        self.game = game
        self.myColor = player

    def timeOut(self):
        if abs(time.time() - self.time) > 20:
            return True

    def search(self, board, turn, curPlayer):
        print(np.array(board))
        x = input()
        x = x.split()
        y = int(x[1])
        x = int(x[0])
        action = self.game.actionRefereeToGame((x,y))
        print(action)
        return action
