import numpy as np
import math
import time

infinity = 9999


WHITE = 1
BLACK = -1
class Absearch():

    def __init__(self, game, player):
        #Player will always be White(1/friend), as we pass in canonical board
        self.game = game
        self.player = player
        self.abpDepth = 4
        # self.pubgPredictModule = PredictModule("pubgParams")

        self.max = {}
        self.min ={}
    def timeOut(self):
        if abs(time.time() - self.time) > 20:
            return True

    def decideAbpDepth(self, total_valid_move, turn):
        assert(total_valid_move <= 48)
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
        v = -infinity
        a = -infinity
        b = infinity

        board = self.game.getCanonicalForm(board, curPlayer)

        self.time = time.time()
        
        valids = np.array(self.game.getValidMoves(board, 1))

        """Forfeit Case"""
        if np.sum(valids[valids == 1]) == 0:
            return self.game.getActionSize()

        """Normal Search"""
        boardString = self.game.stringRepresentation(board)
        #adjust depth according to valid move
        valid_move_count = np.sum(valids[valids == 1])
        
        self.abpDepth = self.decideAbpDepth(valid_move_count, turn)

        # (board, a)
        #Start searching
        if boardString in self.max.keys() and self.abpDepth <= self.max[boardString]["depth"]:
            move = self.max[boardString]["action"]
        else:
            self.max[boardString] = {"depth": -1, "action": None, "value": None}
            move, value = self.alphaBetaSearch((board,1), turn, self.abpDepth, -infinity, infinity, True)
            self.max[boardString]["depth"] = self.abpDepth
            self.max[boardString]["action"] = move
            self.max[boardString]["value"] = value


        e = time.time()

        return move

    def alphaBetaSearch(self, board, turn, depth, a, b, maxPlayer = False):
        if self.timeOut():
            return 0,0

        board, currentP = board
        board = self.game.getCanonicalForm(board, currentP)
        result = self.game.getGameEnded(board, 1, turn)

        boardString = self.game.stringRepresentation(board)
        
        if result != 0:
            return 0,( result if maxPlayer else -result) * 10000
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
                return 0,-self.boardValue(board, turn)
            else:
                #MIN node
                return 0,self.boardValue(board, turn)
        #left Node

        valids = self.game.getValidMoves(board, 1) #8*8*8+1 vector
        results = {}
        if maxPlayer:
            v = -infinity 

            if boardString in self.max.keys() and depth <= self.max[boardString]["depth"]:
                return self.max[boardString]["action"], self.max[boardString]["value"]
            else:
                self.max[boardString] = {"depth": -1, "action": None, "value": None}
                for i in range(len(valids)):
                    if valids[i]:
                        
                        now_friend, now_enemy = self.game.countPieces(board)
                        diff = now_friend -now_enemy
                        next_board, next_curr_player = self.game.getNextState(board, 1, i, turn)
                        next_friend, next_enemy = self.game.countPieces(next_board)
                        next_diff = next_friend - next_enemy

                        if next_diff - diff  >= 0:
                            _, search = self.alphaBetaSearch((next_board, next_curr_player), turn+1, depth-1, a, b ,maxPlayer = False)
                            results[i] = search
                            #print(search, v)
                            v = max(v,search)
                            a = max(a,v)
                            if b <= a:
                                break
                        else:
                            continue

            self.max[boardString]["depth"] = depth
            self.max[boardString]["value"] = v
            try:
                action = max(results, key = results.get)
            except:
                action = self.game.getActionSize()
            self.max[boardString]["action"] = action

            return  action,v
        else:
            v = infinity 

            if boardString in self.min.keys() and depth <= self.min[boardString]["depth"]:
                return self.min[boardString]["action"], self.min[boardString]["value"]
            else:
                self.min[boardString] = {"depth": -1, "action": None, "value": None}

                for i in range(len(valids)):
                    if valids[i]:

                        now_friend, now_enemy = self.game.countPieces(board)
                        diff = now_friend -now_enemy
                        next_board, next_curr_player = self.game.getNextState(board, 1, i, turn)
                        next_friend, next_enemy = self.game.countPieces(next_board)
                        next_diff = next_friend - next_enemy

                        if next_diff - diff  >= 0:
                            _, search = self.alphaBetaSearch((next_board, next_curr_player), turn+1, depth-1, a,b,maxPlayer = True)
                            results[i] = search
                            v = min(v, search)
                            a = min(a,v)
                            if b <= a:
                                break
                        else:
                            continue
            # self.min[boardString] = v 
            self.min[boardString]["depth"] = depth
            self.min[boardString]["value"] = v
            try:
                action = min(results, key = results.get)
            except:
                action = self.game.getActionSize()
            self.min[boardString]["action"] = action
            return action,v      

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
