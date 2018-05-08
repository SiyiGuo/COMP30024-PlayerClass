import numpy as np
from HalfGoLogic import Board, EMPTY, BANNED, WHITE, BLACK, CORNER


class HalfGoGame():
    def __init__(self, n):
        self.n = n

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(self.n)
        return np.array(b.pieces)

    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        """
        use in: 
            for action in range(getActionsize)
        return:
            total number of valid action
        Note:
            somehow there is self.n*self.n + 1 in all Othello and Gobang
            Implementation, why?
            Answer:
                64 notes in the final layer of CNN,
                need to +1 for the bias
                this is why return self.n*self.n + 1
        """

        return self.n*self.n + 1

    def getNextState(self, board, player, action, turn = 1):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
        # 2 = (2,0)
        # currently action = an Integer
        if action == self.n*self.n: 
            return (board, -player)
        b = Board(self.n)
        b.pieces = np.copy(board)
        #even in string representation, we concat column by column
        #picese are grouped by column
        move = (action%self.n, action//self.n,) #(column, row) (int(a/b))
        b.execute_move(move, player)

        return (b.pieces, -player)

    def getValidMoves(self, board, player):
        # return a fixed size binary vector
        # moves, on the same ROWWWWWWWWWWW are grouped together
        valids = [0]*self.getActionSize()
        b = Board(self.n)
        b.pieces = np.copy(board)
        legalMoves =  b.get_legal_moves(player) #in the form (column, row)
        if len(legalMoves)==0:
            valids[-1]=1
            return np.array(valids)
        for x, y in legalMoves:
            valids[self.n*y+x]=1 #since all rows are grouped together
        return np.array(valids)

    def getGameEnded(self, board, player, turn):
        """
        Input:
            board: cannoical board
            player: int, 1 = white, -1 = black
            turn: [0.......23] = 24 turns in total = for i in range(0,24)
        return:
            0 nothing
            1 player Won
            -1 player Lost
        """
        b = Board(self.n)
        b.pieces = np.copy(board)
        if turn < 24: #4: for adding turn parameter
            return 0
        else:
            if b.countDiff(player) > 0:
                return 1
            elif b.countDiff == 0:
                return 1e-4 #tie condiitiion
        
        return -1

    def getCanonicalForm(self, board, player):
        """
        Input:
            Board, 
            player: the perspective
        return:
            current situation of the board in the player's point of view
            1 = friendly army
            -1 = enemy
        Yes! this is correct understanding
        """
        # return player*board
        # board = np.array(board).reshape(8,8)
        result = player*board
        result[result == -3] = CORNER
        # if player == BLACK:
        #     result = np.rot90(result, k = 2)
        return result#.flatten()


    def stringRepresentation(self, board):
        # 8x8 numpy array (canonical board)
        return board.tostring()

    def actionGameToReferee(self, action):
        x = action % 8
        y = action // 8
        return (int(x),int(y))
    
    def actionRefereeToGame(self, action):
        x,y = action
        return y*8+x