import numpy as np
import math
import operator
import time

infinity = 999999

FRIEND = 1
ENEMY = -1
EMPTY = 0


class EvaluationSearch():
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
        """
        :param board: a objective board
        :param turn: the turn
        :param curPlayer: the actual color
        :return:
        """
        board = self.game.getCanonicalForm(board, curPlayer)

        action = self.AggressivePlacing(board)

        if action != 0:
            return action

        if turn == 0:
            """
            The case my color is white
            """
            action = self.game.actionRefereeToGame((4, 4))
            return action
        elif turn == 1:
            """
            the case my actual color is black
            """
            # board[row][column]
            if board[3][4] == ENEMY:
                action = self.game.actionRefereeToGame((3, 4))
            elif board[4][3] == ENEMY:
                action = self.game.actionRefereeToGame((4, 3))
            elif board[3][3] == ENEMY:
                action = self.game.actionRefereeToGame((4, 4))
            elif board[4][4] == ENEMY:
                action = self.game.actionRefereeToGame((3, 3))
            else:
                if board[5][4] == ENEMY or board[4][5] == ENEMY:
                    action = self.game.actionRefereeToGame((3, 3))
                else:
                    action = self.game.actionRefereeToGame((4, 4))
            """ first placing round end"""
            return action
        elif turn == 2 or turn == 3:
            possible_places = [(3, 2), (4, 2), (3, 3), (4, 3), (3, 4), (4, 4)]  # Column, row
            for (column, row) in possible_places:
                if board[row][column] == EMPTY:
                    if not self.dangerousPlace(board, (column, row)):
                        result = (column, row)
                        break

            action = self.game.actionRefereeToGame(result)

            return action

        results = self.evaluateBoard(board)
        action = min(results, key=results.get)
        results.pop(action, None)

        return action

    def AggressivePlacing(self, board):
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for i, row in enumerate(board):
            for j, x in enumerate(row):
                if x == FRIEND:
                    for move in moves:
                        i_dir, j_dir = move
                        if 0 <= i + 2 * i_dir < 6 and 0 <= j + 2 * j_dir < 6:
                            if board[i + i_dir][j + j_dir] == ENEMY and board[i + 2 * i_dir][j + 2 * j_dir] == 0:
                                action = self.game.actionRefereeToGame((j + 2 * j_dir, i + 2 * i_dir))
                                return action
        if board[0][1] == 3 and board[0][2] == 0:
            return self.game.actionRefereeToGame((0, 2))
        if board[7][1] == 3 and board[7][2] == 0:
            return self.game.actionRefereeToGame((0, 2))
        if board[0][6] == 3 and board[0][5] == 0:
            return self.game.actionRefereeToGame((0, 2))
        if board[7][6] == 3 and board[7][5] == 0:
            return self.game.actionRefereeToGame((0, 2))
        return 0

    def dangerousPlace(self, board, action):
        """
        :param action: (column, row)
        :return:
        """
        j, i = action
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for move in moves:
            i_dir, j_dir = move
            if 0 <= i + i_dir < 8 and 0 <= j + j_dir < 8:
                if board[i + i_dir][j + j_dir] == -self.myColor or board[i + i_dir][j + j_dir] == 3:
                    return True
        return False

    def evaluateBoard(self, board):
        """

        :param board: a canonical board
        :return:
        """
        results = {}
        valids = self.game.getValidMoves(board, 1)
        for i in range(len(valids)):
            if valids[i]:
                piece = self.game.actionGameToReferee(i)
                results[i] = self.evaluate(piece, board)
        return results

    def evaluate(self, current, board):
        x1, y1 = current

        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

