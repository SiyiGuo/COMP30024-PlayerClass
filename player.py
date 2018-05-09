import numpy as np
from PubgGame import PubgGame
from HalfGoGame import HalfGoGame
from Search import Search
from Predict import PredictModule
from ABsearch import Absearch

WHITE = 1
BLACK = -1
class Player(object):
    def __init__(self, color):


        self.halfGoPredictModule = PredictModule("halfGoParams")

        # common thing
        self.game = HalfGoGame(8)
        self.myColor = WHITE if color == "white" else BLACK
        self.turn = 0
        self.board = self.game.getInitBoard() # Objective board
        self.predictModule = self.halfGoPredictModule
        self.searchModule = Search(self.game, self.predictModule)
        self.pubgMode = False



    def action(self, turns):
        """
        Call by referee
        ti request an action
        :param turns:
        :return:
        """
        # print(turns, self.turn)
        # recalibrate the turns
        self.turn = turns

        # Use our own coordinate for search, and update board
        action = 0
        if not self.pubgMode:
            action = self.AggressivePlacing()
        if action == 0:
            action = self.search(self.board, turns, self.myColor)

            if self.myColor == BLACK and not self.pubgMode:
                action = 63 - action

            valids = self.game.getValidMoves(self.board,self.myColor)
            while(True):
                action = 0 if action == (len(valids) - 1) else action
                if not valids[action]:
                    action += 1
                elif not self.pubgMode and self.dangerousPlace(action):
                    action += 1
                else:
                    break

        self.board, next_player = self.game.getNextState(self.board, self.myColor, action, self.turn)

        # self.game coordinate -> referee
        print("Action Call: our board:\n%s"%np.array(self.board).reshape(8,8))
        action_referee_form = self.game.actionGameToReferee(action)

        if self.turn == 23 and not self.pubgMode:
            self.game = PubgGame(8)
            self.turn = 0
            print("game switch at turn:%s, %s"%(turns, self.turn))
            self.searchModule = Absearch(self.game, self.myColor)
            self.pubgMode = True

        return action_referee_form


    def update(self, action):
        """
        :param action:
            Placing(x,y);
            Moving((a,b), (c,d));
            No action: None
        :return: void
        """
        self.turn += 1

        action_our_form = self.game.actionRefereeToGame(action)

        self.board, next_player = self.game.getNextState(self.board, -1*self.myColor, action_our_form, self.turn)

        print("update Call: our board:\n%s" % np.array(self.board).reshape(8, 8))
        if self.turn == 23 and not self.pubgMode:
            self.game = PubgGame(8)
            self.turn = 0
            self.searchModule = Absearch(self.game, self.myColor)
            self.pubgMode = True


    def search(self, board, turn, colour):
        return self.searchModule.search(board, turn, colour)
    
    def AggressivePlacing(self):
        moves = [(-1,0), (1,0), (0,-1), (0,1)]
        for i,row in enumerate(self.board):
            for j, x in enumerate(row):
                if x == self.myColor:
                    for move in moves:
                        i_dir, j_dir = move
                        if self.myColor == 1 and 0<= i+2*i_dir < 6 and 0<= j+2*j_dir < 6:
                            if self.myColor == -1 and 1 < i + 2 * i_dir < 8 and 1 < j + 2 * j_dir < 8:
                                if self.board[i+i_dir][j+j_dir] == -self.myColor and self.board[i+2*i_dir][j+2*j_dir] == 0:
                                    action = self.game.actionRefereeToGame((j+2*j_dir,i+2*i_dir))
                                    return action
        return 0

    def dangerousPlace(self, action):
        j,i = self.game.actionGameToReferee(action)
        moves = [(-1,0), (1,0), (0,-1), (0,1)]
        for move in moves:
            i_dir, j_dir = move
            if 0<= i+i_dir < 8 and 0<= j+j_dir < 8:
                if self.board[i+i_dir][j+j_dir] == -self.myColor:
                    return True
        return False


    
