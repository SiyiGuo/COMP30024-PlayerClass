import numpy as np
import math
import operator
import time
from Predict import PredictModule
infinity = 9999


WHITE = 1
BLACK = -1
class Absearch():

    def __init__(self, game, player):
        #Player will always be White(1/friend), as we pass in canonical board
        self.game = game
        self.player = player
        self.abpDepth = 3
        # self.pubgPredictModule = PredictModule("pubgParams")

        self.max = {}
        self.min ={}
    def timeOut(self):
        if abs(time.time() - self.time) > 20:
            return True

    def decideAbpDepth(self, total_valid_move):
        assert(total_valid_move <= 48)
        print(total_valid_move)
        # a = input()
        # if total_valid_move <= 24:
        #     return 8
        return 5
    
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

        self.time = time.time()
        
        valids = np.array(self.game.getValidMoves(board, 1))

        #adjust depth according to valid move
        valid_move_count = np.sum(valids[valids == 1])
        
        self.abpDepth = self.decideAbpDepth(valid_move_count)

        #Start searching
        for i in range(len(valids)):
            if valids[i] == 1:
                print(i, end="\r")
                
                now_friend, now_enemy = self.game.countPieces(board)
                diff = now_friend -now_enemy
                next_board, next_curr_player = self.game.getNextState(board, 1, i, turn)
                next_friend, next_enemy = self.game.countPieces(next_board)
                next_diff = next_friend - next_enemy

                if next_diff - diff  >=  0:
                    results[i] = self.alphaBetaSearch((next_board, next_curr_player), turn+1, self.abpDepth, a,b,False)   
                    v = max(v,results[i])
                    a = max(a,v)     
                    if b <= a:
                        break
                else:
                    # print("silly move, passs:\n%s"%np.array(next_board).reshape(8,8))
                    continue
        e = time.time()

        # print(results)
        try:
            move = max(results, key=results.get)
        except ValueError:
            move = self.game.getActionSize()

        return move

    def alphaBetaSearch(self, board, turn, depth, a, b, maxPlayer = False):
        if self.timeOut():
            return 0

        board, currentP = board
        board = self.game.getCanonicalForm(board, currentP)
        boardString = str(self.game.stringRepresentation(board)) + str(depth)
        result = self.game.getGameEnded(board, 1, turn)


        #left Node
        if result != 0:
            # print("Board:\n%s"%np.array(board.reshape(8,8)))
            # print("result:%s"%result)
            # print("Another result:%s"%self.game.getCanonicalForm(board, currentP))
            if not maxPlayer:
                #case for last layer is max
                if currentP == WHITE:
                    return result* 10000
                else:
                    return -result*10000
            else:
                # case for last layer is min
                if currentP == WHITE:
                    return -result* 10000
                else:
                    return result*10000
        if depth == 0:
            if not maxPlayer:
                # Max Node
                return self.boardValue(board, turn)
            else:
                #MIN node
                return self.boardValue(board, turn)

        valids = self.game.getValidMoves(board, 1) #8*8*8+1 vector

        if maxPlayer:
            v = -infinity 

            # if boardString in self.max: 
            #     return self.max[boardString] 
            if boardString in self.max.keys():
                if depth <= self.max[boardString]["depth"]:
                    return self.max[boardString]["value"]
            else:
                self.max[boardString] = {"depth":-1, "value":None}

            for i in range(len(valids)):
                if valids[i]:
                    
                    now_friend, now_enemy = self.game.countPieces(board)
                    diff = now_friend -now_enemy
                    next_board, next_curr_player = self.game.getNextState(board, 1, i, turn)
                    next_friend, next_enemy = self.game.countPieces(next_board)
                    next_diff = next_friend - next_enemy

                    if next_diff - diff  >= 0:
                        search = self.alphaBetaSearch((next_board, next_curr_player), turn+1, depth-1, a, b ,maxPlayer = False)
                        
                        #print(search, v)
                        v = max(v,search)
                        a = max(a,v)
                        if b <= a:
                            break
                    else:
                        continue

            self.max[boardString]["depth"] = depth
            self.max[boardString]["value"] = v
            # self.max[boardString] = v 
            return v   
        else:
            v = infinity 
            
            # if boardString in self.min: 
            #     return self.min[boardString] 

            if boardString in self.min.keys():
                if depth <= self.min[boardString]["depth"]:
                    return self.min[boardString]["value"]
            else:
                self.min[boardString] = {"depth":-1, "value":None}

            for i in range(len(valids)):
                if valids[i]:

                    now_friend, now_enemy = self.game.countPieces(board)
                    diff = now_friend -now_enemy
                    next_board, next_curr_player = self.game.getNextState(board, 1, i, turn)
                    next_friend, next_enemy = self.game.countPieces(next_board)
                    next_diff = next_friend - next_enemy

                    if next_diff - diff  >= 0:
                        search = self.alphaBetaSearch((next_board, next_curr_player), turn+1, depth-1, a,b,maxPlayer = True)
                        v = min(v, search)
                        a = min(a,v)
                        if b <= a:
                            break
                    else:
                        continue
            # self.min[boardString] = v 
            self.min[boardString]["depth"] = depth
            self.min[boardString]["value"] = v
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
        friendD = self.distancesBetween(friend) 
        value = 100*diff-0.01*friendD
        return value
 
    def distancesBetween(self, pieces): 
        distances = 0 
        for position in pieces: 
            distances+=self.distance(position) 
        return distances 
     
    def distance(self, current): 
        x1,y1 = current 
        x2,y2 = 3.5,3.5 
        return math.sqrt((x1-x2)**2 + (y1-y2)**2) 
