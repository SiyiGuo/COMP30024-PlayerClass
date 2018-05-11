import numpy as np
import math
import operator
import random
import time
from Predict import PredictModule

infinity = 9999


class Top3ExplorSearch():

    def __init__(self, game, player):
        # Player will always be White(1/friend), as we pass in canonical board
        self.game = game
        self.player = player
        self.abpDepth = 4  # Actual Depth = += 1
        self.boards = {}

    def decideAbpDepth(self, total_valid_move, turn):
        assert(total_valid_move <= 48)
        print(total_valid_move)
        if turn in range(185, 192):
            return 8
        elif turn in range(122, 128):
            return 8
        else:
            return 6

    def search(self, board, turn, curPlayer):
        """
        input: A object board
        return: a action number in range(513)
        """

        board = self.game.getCanonicalForm(board, curPlayer)
        boardString = str(self.game.stringRepresentation(board))

        valids = np.array(self.game.getValidMoves(board, 1))
        valid_move_count = np.sum(valids[valids == 1])

        """Forfeit Case"""
        if valid_move_count == 0:
            return self.game.getActionSize()

        """Decide"""
        depth = self.decideAbpDepth(valid_move_count, turn)

        if boardString in self.boards:
            move = self.boards[boardString]
        else:
            move, _ = self.minMax((board, 1), turn, depth, maxPlayer = True)
            self.boards[boardString] = move

        # a = input()
        return move


    def minMax(self, board, turn, depth, maxPlayer=True):

        """must process"""
        board, currentP = board
        board = self.game.getCanonicalForm(board, currentP)
        valids = self.game.getValidMoves(board, 1)  # 8*8*8+1 vector


        """Leaf Note"""
        result = self.game.getGameEnded(board, 1, turn)
        if result != 0:
            if maxPlayer:
                """return value to a min node"""
                return (0, -result * 10000)
            else:
                """return value to a max node"""
                return (0, result * 10000)

        if depth == 0:
            if maxPlayer:
                """return value to a min node"""
                # print(board)
                # print(-self.boardValue(board, turn))
                # a = input()
                return (0, self.boardValue(board, turn))
            else:
                """return value to a max node"""
                return (0, -self.boardValue(board, turn))

        if maxPlayer:
            """Max case"""
            results = {}
            boards = {}
            max3Queue = []
            for action in range(len(valids)):
                if valids[action]:
                    # TODO: Add silly move detector

                    # board, player, action, turn)
                    next_board, next_player = self.game.getNextState(board, 1, action, turn)

                    value = self.boardValue(next_board, turn + 1)

                    boards[action] = next_board

                    if len(max3Queue) <= 3:
                        max3Queue.append((action, value))
                    else:
                        if value > max3Queue[-1][1]:
                            max3Queue[-1] = (action, value)

                    max3Queue = sorted(max3Queue, key=lambda x: x[1])

            for (action, value) in max3Queue:
                next_board, next_player = self.game.getNextState(board, 1, action, turn)
                _, search_value = self.minMax((next_board, next_player), turn + 1, depth - 1, False)
                results[action] = search_value

            try:
                action = max(results, key=results.get)
            except:
                action = self.game.getActionSize()
                results[action] = 0

        elif not maxPlayer:
            """MIN Case"""
            results = {}
            boards = {}
            min3Queue = []
            for action in range(len(valids)):
                if valids[action]:
                    # TODO: Add silly move detector

                    # board, player, action, turn)
                    next_board, next_player = self.game.getNextState(board, 1, action, turn)

                    value = -self.boardValue(next_board, turn + 1)

                    boards[action] = next_board

                    if len(min3Queue) <= 3:
                        min3Queue.append((action, value))
                    else:
                        if value < min3Queue[-1][1]:
                            min3Queue[-1] = (action, value)

                    min3Queue = sorted(min3Queue, key=lambda x: x[1], reverse=True)

            for (action, value) in min3Queue:
                next_board, next_player = self.game.getNextState(board, 1, action, turn)
                _, search_value = self.minMax((next_board, next_player), turn + 1, depth - 1, True)
                results[action] = search_value

            try:
                action = min(results, key=results.get)
            except:
                action = self.game.getActionSize()
                results[action] = 0



        return (action, results[action])

    def boardValue(self, board, turn):
        """
        The higher, the better
        :param board: take a canonical board
        :param turn: the turn index
        :return: a value
        """

        difference_index = 500
        interDistance_index =  -0.5
        toCenterDistance_index = -1

        friend = []
        enemy = []
        for col, row in enumerate(board):
            for row_index, piece in enumerate(row):
                if piece == 1:
                    friend.append((col, row_index))
                elif piece == -1:
                    enemy.append((col, row_index))
        diff = len(friend) - len(enemy)

        interDistance = self.interDistance(friend)

        toCenterDistance = self.toCenterDistance(friend)


        value = difference_index * diff + toCenterDistance_index * toCenterDistance + interDistance * interDistance_index

        return value

    def interDistance(self, pieces):
        length = len(pieces)

        if length == 0:
            return -10000

        sum_x = 0
        sum_y = 0
        for (col, row) in pieces:
            sum_x += col
            sum_y += row

        center_x, center_y = sum_x/length, sum_y/length

        distances = 0
        for position in pieces:
            distances += self.distance(position, (center_x, center_y))
        return distances

    def toCenterDistance(self, pieces):
        distances = 0
        for position in pieces:
            distances += self.distance(position, (3.5, 3.5))
        return distances

    def distance(self, current, target):
        x1, y1 = current
        x2, y2 = target
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

