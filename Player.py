import numpy as np
from PubgGame import PubgGame
from HalfGoGame import HalfGoGame
from Search import Search
from Predict import PredictModule

class Player(object):
    def __init__(self, color):
        # two games
        self.pubg = PubgGame(8)
        self.halfGo = HalfGoGame(8)
        self.pubgPredictModule = PredictModule("pubgParams")
        self.halfGoPredictModule = PredictModule("halfGoParams")

        # common thing
        self.game = self.halfGo
        self.myColor = color
        self.turn = 0
        self.board = self.game.getInitBoard() # Objective board
        self.predictModule = self.halfGoPredictModule
        self.searchModule = Search(self.game, self.predictModule)



    def action(self, turns):
        """
        Call by referee
        ti request an action
        :param turns:
        :return:
        """
        # recalibrate the turns
        self.turn = turns

        # Use our own coordinate for search, and update board
        action = self.search(self.board, turns, self.myColor)
        self.board, next_player = self.game.getNextState(self.board, self.myColor, action)

        # self.game coordinate -> referee
        action_referee_form = self.game.actionGameToReferee(action)

        if self.turn == 23:
            self.game = self.pubg
            self.predictModule = self.pubgPredictModule
            self.searchModule = Search(self.game, self.predictModule)

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

        self.board, next_player = self.game.getNextState(self.board, -1*self.myColor, action_our_form)

        if self.turn == 23:
            self.game = self.pubg
            self.predictModule = self.pubgPredictModule
            self.searchModule = Search(self.game, self.predictModule)
    
    def search(self, board, turn, colour):
        return np.argmax(self.searchModule.search(board, turn, colour))

    
