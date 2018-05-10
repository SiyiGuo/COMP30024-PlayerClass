import numpy as np
import math
import time
infinity = 9999

WHITE = 1
BLACK = -1


class Absearch():

    def __init__(self, game, player):
        # Player will always be White(1/friend), as we pass in canonical board
        self.game = game
        self.player = player
        self.abpDepth = 4
        # self.pubgPredictModule = PredictModule("pubgParams")

        self.max = {}
        self.min = {}

    def timeOut(self):
        if abs(time.time() - self.time) > 20:
            return True

    def decideAbpDepth(self, total_valid_move, turn):
        assert (total_valid_move <= 48)
        print(total_valid_move)
        if turn in range(185, 192):
            return 6
        else:
            return 4
        if turn in range(186, 192):
            return 5
        elif turn in range(122, 128):
            return 5
        else:
            return 3

    def search(self, board, turn, curPlayer):
        """
        input: A canonical board
        return: a action number in range(513)
        """
        s = time.time()
        results = {}
        board = self.game.getCanonicalForm(board, curPlayer)

        self.time = time.time()

        valids = np.array(self.game.getValidMoves(board, 1))

        """Forfeit move"""
        valid_move_count = np.sum(valids[valids == 1])
        if np.sum(valid_move_count) == 0:
            # Case for forfeit move
            return self.game.getActionSize()

        """Normal Search"""
        boardString = self.game.stringRepresentation(board)
        # adjust depth according to valid move

        self.abpDepth = self.decideAbpDepth(valid_move_count, turn)

        if boardString in self.max.keys() and self.abpDepth <= self.max[boardString]["depth"]:
            move = self.max[boardString]["action"]
        else:
            self.max[boardString] = {"depth": -1, "action": None, "value": None}
            move, value = self.alphaBetaSearch((board, 1), turn, self.abpDepth, -infinity, infinity, True)
            self.max[boardString]["depth"] = self.abpDepth
            self.max[boardString]["action"] = move
            self.max[boardString]["value"] = value


        return move


    def boardValue(self, board, turn):
        friend = []
        enemy = []

        # i is column
        # j is row
        # X is the piece
        for col, row in enumerate(board):
            for row_index, piece in enumerate(row):
                if piece == 1:
                    friend.append((col, row_index))
                elif piece == -1:
                    enemy.append((col, row_index))

        diff = len(friend) - len(enemy)
        friendD = self.distancesBetween(friend)
        value = 100 * diff - 0.01 * friendD
        return value

    def distancesBetween(self, pieces):
        distances = 0
        for position in pieces:
            distances += self.distance(position)
        return distances

    def distance(self, current):
        x1, y1 = current
        x2, y2 = 3.5, 3.5
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
