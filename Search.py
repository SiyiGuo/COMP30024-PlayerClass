class Search(object):
    def __init__(self, game, predictModule):
        """
        :param game: the game for this search module
        :param predictModule: modeule that do the prediction
        """

    def search(self, objectBoard, turn, curPlayer):
        """
        :param canonicalBoard: the ObjectBoard
        :param turn: the turn number
        :param curPlayer: current player
        :return: action, in game coordinate, that play it
        """
        canonicalBoard = self.game.getCanonicalForm(objectBoard, curPlayer)


        action, v = self.predictModule.predict(canonicalBoard, turn, curPlayer)
        return action