import numpy as np
import math
import operator
import time
from Predict import PredictModule
infinity = 999999

class Absearch():

    abpDepth = 8 # actual depth = abpdepth + 1
    max = {}
    min = {}

    def __init__(self, game, player):
        #Player will always be White(1/friend), as we pass in canonical board
        self.game = game
        self.player = player
        self.abpDepth = 4
        self.pubgPredictModule = PredictModule("pubgParams")
    
    def timeOut(self):
        if abs(time.time() - self.time) > 20:
            return True

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

        board = self.game.getCanonicalForm(board, curPlayer)

        valids = self.game.getValidMoves(board, 1)
        self.time = time.time()
        
        for i in range(len(valids)):
            if valids[i]:
                # print(i)
                
                results[i] = self.alphaBetaSearch(self.game.getNextState(board, 1, i, turn), turn+1, self.abpDepth, a,b,False)   
                v = max(v,results[i])
                a = max(a,v)     
                if b <= a:
                    break
        e = time.time()

        # print(results)
        try:
            move = max(results, key=results.get)
        except ValueError:
            move = None

        return move

    def alphaBetaSearch(self, board, turn, depth, a, b, maximizingPlayer = False):
        if self.timeOut():
            return 0
        board, currentP = board
        board = self.game.getCanonicalForm(board, currentP)
        boardString = str(self.game.stringRepresentation(board))+str(depth)
        # result = self.game.getGameEnded(board, currentP, turn)
        result = self.game.getGameEnded(board, 1, turn)
        if result != 0:
            # print("Board:\n%s"%np.array(board.reshape(8,8)))
            # print("result:%s"%result)
            # print("Another result:%s"%self.game.getCanonicalForm(board, currentP))
            return (1 if result*currentP == self.player else (-1)) * 10000
        if depth == 0:
            return self.boardValue(board, turn)
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
                    search = self.alphaBetaSearch(self.game.getNextState(board, currentP, i, turn), turn+1, depth-1, a,b,True)
                    v = min(v, search)
                    a = min(a,v)
                    if b <= a:
                        break
            self.min[boardString] = v
            return v       

    def boardValue(self,board,turn):
        return self.pubgPredictModule.predict(board, turn)
        
