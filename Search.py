import math
import numpy as np

class Search(object):
    def __init__(self, game, predictModule):
        """
        :param game: the game for this search module
        :param predictModule: modeule that do the prediction
        """
        self.game = game
        self.predictModule = predictModule
        self.Qsa = {}       # stores Q values for s,a (as defined in the paper) || the reward for current move a
        self.Nsa = {}       # stores #times edge s,a was visited || the # of time we have taking action a in current situation
        self.Ns = {}        # stores #times board s was visited || the # of this situation we have been in 
        self.Ps = {}        # stores initial policy (returned by neural net)

        self.Es = {}        # stores game.getGameEnded ended for board s || Store the gaming result of current board situation
        self.Vs = {}        # stores game.getValidMoves for board s

    def search(self, objectBoard, turn, curPlayer):
        """
        :param canonicalBoard: the ObjectBoard
        :param turn: the turn number
        :param curPlayer: current player
        :return: action, in game coordinate, that play it
        """
        canonicalBoard = self.game.getCanonicalForm(objectBoard, curPlayer)
        for x in range(25):
            self.explore(canonicalBoard, turn)

        s = self.game.stringRepresentation(canonicalBoard)
        counts = [self.Nsa[(s,a)] if (s,a) in self.Nsa else 0 for a in range(self.game.getActionSize())]

        # debug check
        if (float(sum(counts)) ==0):
            print("\nerror in MCTS.getActionProb, before deciding action")
            print("turnindex:%s"%turn)
            print(canonicalBoard.reshape(8,8))
            print("non existing pattern: \n %s"%np.fromstring(s, dtype=int).reshape(8,8)) #could add reshape here
            exit()

        #could remove temp? as it is always 1
        counts = [x**(1./1) for x in counts]

        #may need to mask probs
        # curr_player =  WHITE if turn % 2 == 0 else BLACK
        valids = self.game.getValidMoves(canonicalBoard, 1)
        probs = [x/float(sum(counts)) for x in counts] # *valids

        #Mask the invalid probability
        return np.argmax(np.array(probs) * np.array(valids))
    
    def explore(self, board, turn):
        s = self.game.stringRepresentation(board)

        curPlayer = 1 if turn % 2 == 0 else -1

        if turn < 24:
            self.Es[s] = 0
        else:
            self.Es[s] = self.game.getGameEnded(board, 1, turn)
        
        if self.Es[s]!=0:
            return -self.Es[s]
        
        if s not in self.Ps:

            self.Ps[s], v = self.predictModule.predict(board, turn)
        
            valids = self.game.getValidMoves(board, curPlayer)
            
            before_mask = np.array(self.Ps[s][:-1])
            self.Ps[s] = self.Ps[s]*valids

            sum_Ps_s = np.sum(self.Ps[s])
            if sum_Ps_s > 0:
                self.Ps[s] /= sum_Ps_s    
            else:
                self.Ps[s] = self.Ps[s] + valids
                self.Ps[s] /= np.sum(self.Ps[s])
            self.Vs[s] = valids
            self.Ns[s] = 0
            return -v
        valids = self.Vs[s]
        cur_best = -float('inf')
        best_act = -1
        for a in range(self.game.getActionSize()):
            if valids[a]:
                if (s,a) in self.Qsa:
                    u = self.Qsa[(s,a)] +1.0*self.Ps[s][a]*math.sqrt(self.Ns[s])/(1+self.Nsa[(s,a)])
                else:

                    u = 1.0*self.Ps[s][a]*math.sqrt(self.Ns[s])     # Q = 0 ?

                if u > cur_best:
                    cur_best = u
                    best_act = a
        a = best_act

        #assert invalid move
        if curPlayer == 1:
            try:
                assert a<48 #index of first column, sixth row
            except:
                print("Player: %s, action: %s, turn: %s, board:\n%s"%(curPlayer, a, turn, board.reshape(8,8)))
                exit()
        elif curPlayer == -1:
            try:
                assert a > 15 #index of last column, second row
            except:
                print("Player: %s, action: %s, turn: %s, board:\n%s"%(curPlayer, a, turn, board.reshape(8,8)))
                exit()

        # 1 = friendly, as this is self-play on each turn
        # so: next_player is always -1
        # -1 means enemy, not BLACK
        next_s, next_player = self.game.getNextState(board, 1, a) 

        # substitute ourself to another player, 
        next_s = self.game.getCanonicalForm(next_s, next_player) 
        
        # search for it
        v = self.explore(next_s, turn + 1)
    
        if (s,a) in self.Qsa:
            self.Qsa[(s,a)] = (self.Nsa[(s,a)]*self.Qsa[(s,a)] + v)/(self.Nsa[(s,a)]+1)
            self.Nsa[(s,a)] += 1
        else:
            self.Qsa[(s,a)] = v
            self.Nsa[(s,a)] = 1

        self.Ns[s] += 1
        return -v


