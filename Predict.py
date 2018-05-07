class PredictModule(object):
    def __init__(self, directory_name):
        self.path = directory_name # TODO: this need to open folder under current directory
        self.params = {}

    def predict(self, canonicalBoard, turn, curPlayer):
        """
        :param canonicalBoard: the board in curPlayer's pov. 1 is friend, -1 is enemy
        :param turn: the current turn number(could -24 for pubg)
        :param curPlayer: the color of current player
        :return: action: the best action to win, v: the winning prob
        """
        action = -1
        v = -1
        return action, v

    def read_params(self):
        """
        Read from self.params
        :return:  a dictionary of all module
        """
        params = {}
        return params

