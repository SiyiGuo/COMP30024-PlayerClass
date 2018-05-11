import numpy as np
import math
import operator
import random
import time
from Predict import PredictModule

infinity = 999999


class Top3ExplorSearch():

    def __init__(self, game, player):
        # Player will always be White(1/friend), as we pass in canonical board
        self.game = game
        self.player = player
        self.abpDepth = 3  # Actual Depth = += 1
        self.boards = {}

    def search(self, board, turn, curPlayer):
        """
        input: A canonical board
        return: a action number in range(513)
        """
        board = self.game.getCanonicalForm(board, curPlayer)
        boardString = str(self.game.stringRepresentation(board))
        if boardString in self.boards:
            move = self.boards[boardString]
        else:
            move, _ = self.minMax((board, 1), turn, self.abpDepth, True)
            self.boards[boardString] = move
        print(move)
        return move


    def minMax(self, board, turn, depth, maximizingPlayer=True):

        board, currentP = board
        board = self.game.getCanonicalForm(board, currentP)
        result = self.game.getGameEnded(board, 1, turn)
        if result != 0:
            return (0, (result if maximizingPlayer else -result) * 10000)
        if depth == 0:
            return (0, -1 if maximizingPlayer else 1 * self.boardValue(board, turn))

        valids = self.game.getValidMoves(board, 1)  # 8*8*8+1 vector
        results = {}
        if maximizingPlayer:

            max3Queue = []
            for action in range(len(valids)):
                if valids[action]:
                    # TODO: Add silly move detector

                    # board, player, action, turn)
                    next_board, next_player = self.game.getNextState(board, currentP, action, turn)
                    value = self.boardValue(next_board, turn + 1)

                    # TODO: change to depth
                    if len(max3Queue) <= 3:
                        max3Queue.append((action, value))
                    else:
                        if value > max3Queue[-1][1]:
                            max3Queue[-1] = (action, value)

                    max3Queue = sorted(max3Queue, key=lambda x: x[1])
            print("curPlayer", currentP)
            for (action, value) in max3Queue:
                _, search = self.minMax(self.game.getNextState(board, -currentP,  action,  turn), turn + 1, depth - 1,
                                        False)
                results[action] = search

            try:
                action = max(results, key=results.get)
            except:
                action = self.game.getActionSize()
            return (action, results[action])

        else:

            min3Queue = []
            for action in range(len(valids)):
                if valids[action]:
                    # TODO: Add silly move detector

                    next_board, next_player = self.game.getNextState(board, currentP, action,  turn)
                    value = self.boardValue(next_board, turn + 1)

                    if len(min3Queue) <= 3:
                        min3Queue.append((action, value))
                    else:
                        if value < min3Queue[-1][1]:
                            min3Queue[-1] = (action, value)

                    min3Queue = sorted(min3Queue, key=lambda x: x[1], reverse=True)

            for (action, value) in min3Queue:
                _, search = self.minMax(self.game.getNextState(board, -currentP, action, turn), turn + 1, depth - 1,
                                        True)
                results[action] = search

            try:
                action = min(results, key=results.get)
            except:
                action = self.game.getActionSize()

            return (action, results[action])

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
        return (100 * diff - 0.01 * friendD)

    def distancesBetween(self, pieces):
        distances = 0
        for position in pieces:
            distances += self.distance(position)
        return distances

    def distance(self, current):
        x1, y1 = current
        x2, y2 = 3.5, 3.5
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

