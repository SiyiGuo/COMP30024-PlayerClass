import numpy as np
import math
import operator
import time

infinity = 999999

class ABplacing():

     # actual depth = abpdepth + 1
    max = {}
    min = {}
    nearby = [-9,-8,-7,-1,1,7,8,9]

    def __init__(self, game, player):
        #Player will always be White(1/friend), as we pass in canonical board
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
        s = time.time()
        results = {}
        v = -infinity
        a = -infinity
        b = infinity
        # print(board)
        board = self.game.getCanonicalForm(board, curPlayer)
        # print(board)
        valids = self.game.getValidMoves(board, 1)
        self.time = time.time()
        # print(valids)
        for i in range(len(valids)):
            if valids[i]:
                # print(i)
                near = 0
                for dir in self.nearby:
                    place = i+dir
                    if 0<place<len(valids):
                        x,y = self.game.actionGameToReferee(place)
                        if abs(board[x][y]) == 1:
                            near = 1
                            break
                if near == 0:
                    # print(i)
                    # print("no nearby")
                    continue
                results[i] = self.alphaBetaSearch(self.game.getNextState(board, 1, i, turn), turn+1, self.abpDepth, a,b,False)   
                v = max(v,results[i])
                a = max(a,v)     
                if b <= a:
                    break
        e = time.time()

        # print(results)
        move = max(results, key=results.get)
        return move

    def alphaBetaSearch(self, board, turn, depth, a, b, maximizingPlayer = False):
        # print(depth)
        if self.timeOut():
            return 0
        board, currentP = board
        board = self.game.getCanonicalForm(board, currentP)
        boardString = str(self.game.stringRepresentation(board))+str(depth)
        # result = self.game.getGameEnded(board, currentP, turn)
        result = self.game.getGameEnded(board, 1, turn)
        if result != 0:
            return (-result if maximizingPlayer else result * 10000)
        if depth == 0:
            return ( -1 if maximizingPlayer else 1 * self.boardValue(board, turn))
        valids = self.game.getValidMoves(board, 1) #8*8*8+1 vector
        if maximizingPlayer:
            v = -infinity 
            if boardString in self.max:
                return self.max[boardString]
            for i in range(len(valids)):
                if valids[i]:
                    search = self.alphaBetaSearch(self.game.getNextState(board, currentP, i, turn), turn+1, depth-1, a, b ,False)
                    
                    #print(search, v)
                    v = max(v,search)
                    a = max(a,v)
                    if b <= a:
                        break
            self.max[boardString] = v
            return v   
        else:
            v = infinity 
            if boardString in self.min:
                return self.min[boardString]
            for i in range(len(valids)):
                if valids[i]:
                    if boardString in self.min:
                        search = self.min[boardString]
                    else:
                        search = self.alphaBetaSearch(self.game.getNextState(board, currentP, i, turn), turn+1, depth-1, a,b,True)
                        self.min[boardString] = search
                    v = min(v, search)
                    a = min(a,v)
                    if b <= a:
                        break
            self.min[boardString] = v
            return v       

    def boardValue(self,board,turn):
        friend = []
        enemy = []

        #i is column
        #j is row
        #X is the piece
        for col,row in enumerate(board):
            for row_index,piece in enumerate(row):
                if piece == 1:
                    friend.append((col,row_index))
                elif piece == -1:
                    enemy.append((col,row_index))

        diff = len(friend) - len(enemy)
        friendD = self.distancesBetweenMiddle(friend)
        return (200*diff-0.01*friendD)

    def distancesBetweenMiddle(self, pieces):
        distances = 0
        for position in pieces:
            distances+=self.distance(position)
        return distances
    
    def distance(self, current):
        x1,y1 = current
        x2,y2 = 3.5,3.5
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)
        
