import numpy as np
import math
import operator
import time

infinity = 999999

FRIEND = 1
ENEMY = -1
class HardCodeSearch():
    """
    NOTE: 
    in this module, all things based on canonical board,
    and use coordinate (column, row)
    """

    def __init__(self, game, player):
        #Player will always be White(1/friend), as we pass in canonical board
        self.game = game
        self.myColor = player
    
    def timeOut(self):
        if abs(time.time() - self.time) > 20:
            return True

    def search(self, board, turn, curPlayer):
        board = self.game.getCanonicalForm(board, curPlayer)
        
        action = 0
        action = self.AggressivePlacing(board)
        if action != 0:
            return action

        if turn == 0:
            """
            The case my color is white
            """
            action = self.game.actionRefereeToGame((4,4))
            return action
        elif turn == 1:
            """
            the case my actual color is black
            """
            if board[3][4] == ENEMY:
                action = self.game.actionRefereeToGame((3,4)) 
            elif board[4][3] == ENEMY:
                action = self.game.actionRefereeToGame((4,3)) 
            elif board[3][3] == ENEMY:
                action = self.game.actionRefereeToGame((4,4)) 
            elif board[4][4] == ENEMY:
                action = self.game.actionRefereeToGame((3,3)) 
            else:
                action = self.game.actionRefereeToGame((4,4))
            """ first placing round end"""
            return action
        elif turn == 2 or turn == 3:
            if board[3][3] == ENEMY:
                action = self.game.actionRefereeToGame((5,3))
            elif board[3][2] == ENEMY:
                action = self.game.actionRefereeToGame((3,4))
            elif board[2][3] == ENEMY:
                action = self.game.actionRefereeToGame((4,3))
            else:
                action = self.game.actionRefereeToGame((3,3))
            return action
        distances = self.DistanceToCenter(board)
        action = min(distances, key=distances.get)
        print(distances)
        return action

    def AggressivePlacing(self, board):
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for i, row in enumerate(board):
            for j, x in enumerate(row):
                if x == FRIEND:
                    for move in moves:
                        i_dir, j_dir = move
                        if 0<= i+2*i_dir < 6 and 0<= j+2*j_dir < 6:
                            if board[i+i_dir][j+j_dir] == ENEMY and board[i+2*i_dir][j+2*j_dir] == 0:
                                action = self.game.actionRefereeToGame((j+2*j_dir,i+2*i_dir))
                                return action
        if board[0][1] == 3 and board[0][2] == 0:
            return self.game.actionRefereeToGame((0,2))
        if board[7][1] == 3 and board[7][2] == 0:
            return self.game.actionRefereeToGame((0,2))
        if board[0][6] == 3 and board[0][5] == 0:
            return self.game.actionRefereeToGame((0,2))
        if board[7][6] == 3 and board[7][5] == 0:
            return self.game.actionRefereeToGame((0,2))
        return 0

    def dangerousPlace(self, action):
        j,i = action
        moves = [(-1,0), (1,0), (0,-1), (0,1)]
        for move in moves:
            i_dir, j_dir = move
            if 0<= i+i_dir < 8 and 0<= j+j_dir < 8:
                if self.board[i+i_dir][j+j_dir] == -self.myColor or self.board[i+i_dir][j+j_dir] == 3:                    
                    return True
        return False
    
    def DistanceToCenter(self,board):
        friend = [[],[]]

        #i is column
        #j is row
        #X is the piece
        for col,row in enumerate(board):
            for row_index,piece in enumerate(row):
                if piece == 1:
                    friend[0].append(col)
                    friend[1].append(row_index)
        center = self.centeroidnp(friend)
        print(center)
        distances = {}
        valids = self.game.getValidMoves(board,1)
        for i in range(len(valids)):
            if valids[i]:
                piece = self.game.actionGameToReferee(i)
                distances[i] = self.distance(piece,center)
        return distances 
    
    def distance(self, current, target):
        x1,y1 = current
        x2,y2 = target
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)
    
    def centeroidnp(self,arr):
        length = len(arr[0])
        sum_x = np.sum(arr[0])
        sum_y = np.sum(arr[1])
        return sum_y/length, sum_x/length
