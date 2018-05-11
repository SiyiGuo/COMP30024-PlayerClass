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
        self.abpDepth = 6  # Actual Depth = += 1
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
            return (0, result * 10000)
        if depth == 0:
            return (0, self.boardValue(board, turn))

        valids = self.game.getValidMoves(board, 1)  # 8*8*8+1 vector
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

                # TODO: change to depth
                if len(max3Queue) <= 3:
                    max3Queue.append((action, value))
                else:
                    if value > max3Queue[-1][1]:
                        max3Queue[-1] = (action, value)

                max3Queue = sorted(max3Queue, key=lambda x: x[1])
        for (action, value) in max3Queue:
            print(boards[action])
            print(value)
            a = input()
            _, search = self.minMax(self.game.getNextState(board, 1,  action,  turn), turn + 1, depth - 1,
                                    False)
            results[action] = search

        try:
            action = max(results, key=results.get)
        except:
            action = self.game.getActionSize()
        return (action, results[action])

    def boardValue(self, board, turn):
        """
        :param board: take a canonical board
        :param turn: the turn index
        :return: a value
        """

        difference_index = 100
        interDistance_index = 0.01
        toCenterDistance_index = 0.01

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


        value = difference_index * diff + \
                toCenterDistance_index * toCenterDistance + \
                interDistance * interDistance_index

        return value

    def interDistance(self, pieces):
        length = len(pieces[0])
        sum_x = np.sum(pieces[0])
        sum_y = np.sum(pieces[1])
        center_x, center_y = sum_y/length, sum_x/length

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

