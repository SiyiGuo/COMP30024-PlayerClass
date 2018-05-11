from HalfGoGame import HalfGoGame
from PubgGame import PubgGame

#Moving module
from ABsearch import Absearch
from MinMaxSearch import MinMaxSearch
from Top3ExplorSearch import Top3ExplorSearch

# placing module
from HardCodeSearch import HardCodeSearch
from WhiteEvaluationSearch import WhiteEvaluationSearch
from BlackEvaluationSearch import BlackEvaluationSearch

WHITE = 1
BLACK = -1
class Player(object):
    def __init__(self, color):

        # common thing
        self.game = HalfGoGame(8)
        self.myColor = WHITE if color == "white" else BLACK
        self.turn = 0
        self.board = self.game.getInitBoard() # Objective board
        self.pubgMode = False
        self.pubg = PubgGame(8)


        """different placing module"""
        if self.myColor == WHITE:
            self.searchModule = WhiteEvaluationSearch(self.game, self.myColor)
        else:
            self.searchModule = BlackEvaluationSearch(self.game, self.myColor)

        """different moving module"""
        # self.predictModule = self.pubgPredictModule
        # self.searchModule = Absearch(self.pubg, self.myColor)
        # self.pubgMoveSearchModule = MinMaxSearch(self.pubg, self.myColor)
        self.pubgMoveSearchModule = Top3ExplorSearch(self.pubg, self.myColor)




    def action(self, turns):
        """
        Call by referee
        ti request an action
        :param turns:
        :return:
        """
        # recalibrate the turns
        self.turn = turns
        # print(turns, self.turn)

        # Use our own coordinate for search, and update board
        action = self.search(self.board, turns, self.myColor)

        if self.myColor == BLACK and not self.pubgMode:
            action = 63 - action

        self.board, next_player = self.game.getNextState(self.board, self.myColor, action, self.turn)

        # self.game coordinate -> referee
        if action == self.game.getActionSize():
            action_referee_form = None
        else:
            action_referee_form = self.game.actionGameToReferee(action)

        if self.turn == 23 and not self.pubgMode:
            self.game = self.pubg
            self.turn = 0
            self.searchModule = self.pubgMoveSearchModule
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

        if action == None:
            action_our_form = self.game.getActionSize()
        else:
            action_our_form = self.game.actionRefereeToGame(action)

        self.board, next_player = self.game.getNextState(self.board, -1 * self.myColor, action_our_form, self.turn)

        if self.turn == 23 and not self.pubgMode:
            self.game = self.pubg
            self.turn = 0
            self.searchModule = self.pubgMoveSearchModule
            self.pubgMode = True

    def search(self, board, turn, colour):
        return self.searchModule.search(board, turn, colour)



