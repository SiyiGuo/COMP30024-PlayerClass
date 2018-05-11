import numpy as np
import math
import operator
import time


FRIEND = 1
ENEMY = -1
EMPTY = 0


class WhiteEvaluationSearch():
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
        action = 0
        action = self.AggressivePlacing(board)
        if action != 0:
            return action
        if turn == 0:
            """
            The case my color is white
            """
            action = self.game.actionRefereeToGame((4, 4))
            return action
        elif turn == 2:
            if self.dangerousPlace(board, (4, 4)):
                action = self.evaluateBoard(board)
                return action
            possible_places = [(3, 2), (4, 2), (3, 3), (4, 3), (3, 4), (4, 4)]  # Column, row
            for (column, row) in possible_places:
                if board[row][column] == EMPTY:
                    if not self.dangerousPlace(board, (column, row)):
                        result = (column, row)
                        break

            action = self.game.actionRefereeToGame(result)

            return action

        action = self.evaluateBoard(board)

        return action

    def AggressivePlacing(self, board):
        possibleMoves = {}
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for i, row in enumerate(board):
            for j, x in enumerate(row):
                if x == FRIEND:
                    for move in moves:
                        i_dir, j_dir = move
                        if 0 <= i + 2 * i_dir < 6 and 0 <= j + 2 * j_dir < 8:
                            if board[i + i_dir][j + j_dir] == ENEMY and board[i + 2 * i_dir][j + 2 * j_dir] == 0:
                                action = self.game.actionRefereeToGame((j + 2 * j_dir, i + 2 * i_dir))
                                possibleMoves[action] = i+2*i_dir
        if board[0][1] == 3 and board[0][2] == 0:
            possibleMoves[self.game.actionRefereeToGame((0, 2))] = 2
        if board[7][1] == 3 and board[7][2] == 0:
            possibleMoves[self.game.actionRefereeToGame((7, 2))] = 2
        if board[0][6] == 3 and board[0][5] == 0:
            possibleMoves[self.game.actionRefereeToGame((0, 5))] = 5
        if board[7][6] == 3 and board[7][5] == 0:
            possibleMoves[self.game.actionRefereeToGame((7, 5))] = 5
        try:
            action = min(possibleMoves, key = possibleMoves.get)
        except:
            action = 0
        return action

    def dangerousPlace(self, board, action):
        """
        :param action: (column, row)
        :return:
        """
        j, i = action
        if j < 2:
            return False
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for move in moves:
            i_dir, j_dir = move
            if 0 <= i + i_dir < 8 and 0 <= j + j_dir < 8:
                if (board[i + i_dir][j + j_dir] == -self.myColor or board[i + i_dir][j + j_dir] == 3) and board[i - i_dir][j - j_dir] != self.myColor and i - i_dir > 2:
                    return True
        return False

    def evaluateBoard(self, board):
        """

        :param board: a canonical board
        :return: an optimal pos
        """
        results = np.zeros([8,4]) # col row

        i = 16
        while i < 48:
            col, row = i%8, i//8
            if i < 24:
                results[col][row-2] += 2
            if board[row][col]==1:
                results = self.updateSides(results, (col,row), 1)
                results = self.updateCorners(results, (col, row), 1)
            elif board[row][col]==-1:
                results = self.updateSides(results, (col,row), -2)
                results = self.updateCorners(results, (col, row), 1)
                results = self.updateDefence(board, results, (col, row), 2)
                results = self.updateTake(board, results, (col, row), 2)
            results[col][row-2] -= self.distanceToCenter((col,row))
            i +=1
        valids = self.game.getValidMoves(board, 1)

        # print(np.array(results).T)
        for i in range(len(valids)):
            if 15< i < 48 and not valids[i]:
                col, row = i%8, i//8
                col, row = col, row-2
                # print(col,row)
                results[col, row] = 0

        max = -100
        for col, x in enumerate(results):
            for row, y in enumerate(x):
                if y>max:
                    max = y
                    action = col, row+2
        print(np.array(results).T)

        return self.game.actionRefereeToGame((action))

    def updateSides(self, results, pos, value):
        sides = [(1,0),(-1,0),(0,1),(0,-1)]
        col, row = pos
        col, row = col, row - 2
        for dir in sides:
            col_dir, row_dir = dir
            if 0 <= col+col_dir < 8 and 0<= row+row_dir < 4:
                results[col+col_dir][row+row_dir] += value
        return results

    def updateCorners(self, results, pos, value):
        sides = [(1,1),(-1,1),(1,-1),(-1,-1)]
        col, row = pos
        col, row = col, row - 2
        for dir in sides:
            col_dir, row_dir = dir
            if 0 <= col+col_dir < 8 and 0<= row+row_dir < 4:
                results[col+col_dir][row+row_dir] += value
        return results

    def updateDefence(self, board, results, pos, value):
        sides = [(1,0),(-1,0),(0,1),(0,-1)]
        col, row = pos
        res_col, res_row = col, row - 2
        for dir in sides:
            col_dir, row_dir = dir
            if 0 <= res_col+2*col_dir < 8 and 0<= res_row+2*row_dir < 4 and board[row+row_dir][col+col_dir] == 1:
                results[res_col+2*col_dir][res_row+2*row_dir] += value
        return results

    def updateTake(self, board, results, pos, value):
        sides = [(1,0),(-1,0),(0,1),(0,-1)]
        col, row = pos
        res_col, res_row = col, row - 2
        for dir in sides:
            col_dir, row_dir = dir
            if 0 <= res_col+col_dir < 8 and 0<= res_row+row_dir < 4:
                pass
            else:
                continue
            if 0 <= res_col+2*col_dir < 8 or 0<= res_row+2*row_dir < 4 or board[row+2*row_dir][col+2*col_dir] == 1:
                results[res_col+col_dir][res_row+row_dir] += value
        return results

    def distanceToCenter(self, pos):
        x,y = pos
        return 0.1*math.sqrt((x-3.5)**2 + (y-3.5)**2)

