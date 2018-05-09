from PubgLogic import Board, WHITE, BLACK, EMPTY, BANNED, CORNER
import numpy as np


# coordinate system: (column, row)
class PubgGame():
    def __init__(self, n):
        """
        input:\n
            n: board size
        """
        self.n = n

    def getInitBoard(self, obBoard = None):
        """

        :param obBoard: numpy array of 1*64
        :return: numpy array
        """
        board = Board(self.n, obBoard)
        return np.array(board.pieces)
    
    def getBoardSize(self):
        """
        :return: the size of the board
        """
        return (self.n, self.n)
    
    def getActionSize(self):
        """
        64 piece each with 8 direction
        +1 for the bias of pi vector
        """
        return 8*8*8 + 1
    
    def getNextState(self, board, player, action, turn):
        """
        Input:
            board: current object board as np array
            player: current player (1 or -1)
            action: an Integer Number in range(513)
        Returns:
            nextBoard: board after applying action,
            nextPlayer: player who plays in the next turn (should be -player)
        
        Turn1: turn = 0
        Turn 128: turn = 127
        First Shrink
        Turn 129: turn = 128
        Turn 192: turn = 191
        Second Srhink
        Turn 193: turn = 192
        """
        
        board = Board(self.n, np.copy(board))
        
        if action != None and action != self.getActionSize():
            #Case there is no move
            #Move piece first
            piece_index = action // 8
            direction_index = action % 8
            direction = board.direction_combine[direction_index] #note in board, it is row, column
            y_dir, x_dir = direction

            piece_column, piece_row = piece_index //8, piece_index % 8
            # print("Pubg Game, turn:%s, action:%s, piece_index:%s, piece_cor:%s, %s, direction_index:%s, direction:%s"%(turn, action, piece_index, piece_column, piece_row, direction_index, direction))
            action = {}
            action["orig"] = (piece_column, piece_row)
            action["dest"] = (piece_column + x_dir, piece_row + y_dir)
            # print("Pubg Game Piece:%s, %s, From:%s to :%s"%(piece_column, piece_row, action["orig"], action["dest"]))
            # print("PubgGame (column, row): \n%s"%board.pieces)
            board.executeMove(action["orig"], action["dest"])

        #After turn 127 has made move, shrink baord now
        if turn == 127:
            # print("board shink")
            board.shrink(turn)
        if turn == 191:
            # print("board shink twice")
            board.shrink(turn)
            board.shrink(turn)
        return (np.copy(board.pieces), -player)

    def getValidMoves(self, board, player):
        """
        Input:
            board: current board
            player: current player's color

        Returns:
            validMoves: a binary vector of length self.getActionSize(), 1 for
                        moves that are valid from the current board and player,
                        0 for invalid moves
        """
        moves = []
        board = Board(self.n, np.copy(board))
        for x in range(self.n):
            for y in range(self.n):
                if board.pieces[y][x] == player: #column, row -> row, column, as board.pieces is in PubgLogic
                    pieceMove = board.getValidMoveForPiece((x,y))
                    moves += pieceMove #pass in column, row index
                else:
                    moves += [0] * 8
        #for bias vector
        moves += [0]
        assert(len(moves) == 8*8*8+1)
        return moves

    def getGameEnded(self, board, player, turn):
        """
        Input:
            board: current object board
            player: current player (1(WHITE) or -1(BLACK))

        Returns:
            r: 0 if game has not ended. 1 if player won, -1 if player lost,
               small non-zero value for draw. (eg: 1e-4)
               
        """
        board = Board(self.n, np.copy(board))
        blackCount, whiteCount = board.countPieces()
        
        if turn >= 256:
            if whiteCount == blackCount:
                return 1e-4 #tie
            elif whiteCount > blackCount:
                return WHITE*player #white wwin
            elif blackCount > whiteCount:
                return BLACK*player #black win
        if whiteCount < 2 and blackCount < 2:
            return 1e-4 #tie
        if whiteCount < 2:
            return BLACK*player #black win
        if blackCount < 2:
            return WHITE*player #white wwin
        
        return 0 #not ended

    def getCanonicalForm(self, board, player):
        """
        Input:
            board: current object board
            player: current player (1 or -1)

        Returns:
            canonicalBoard: returns canonical form of board. The canonical form
                            should be independent of player. For e.g. in chess,
                            the canonical form can be chosen to be from the pov
                            of white. When the player is white, we can return
                            board as is. When the player is black, we can invert
                            the colors and return the board.
        """

        result = player*board
        result[result == -9] = BANNED
        result[result == -3] = CORNER
        return result

    def stringRepresentation(self, board):
        """
        Input:
            board: current board

        Returns:
            boardString: a quick conversion of board to a string format.
                         Required by MCTS for hashing.
        """
        return board.tostring()

    def actionGameToReferee(self, action):
        direction_combine = [(-1,0), (1,0), (0,-1), (0,1), (-2,0), (2,0), (0,-2), (0,2)]

        piece_index = action // 8
        direction_index = action % 8
        direction = direction_combine[direction_index] #note in board, it is row, column
        y_dir, x_dir = direction

        piece_column, piece_row = piece_index //8, piece_index % 8
        # print("Pubg Game, turn:%s, action:%s, piece_index:%s, piece_cor:%s, %s, direction_index:%s, direction:%s"%(turn, action, piece_index, piece_column, piece_row, direction_index, direction))
        action = {}
        action["orig"] = (piece_column, piece_row)
        action["dest"] = (piece_column + x_dir, piece_row + y_dir)
        # print(action)
        return (action["orig"],action["dest"])
    
    def actionRefereeToGame(self, action):
        direction_combine = [(-1,0), (1,0), (0,-1), (0,1), (-2,0), (2,0), (0,-2), (0,2)]
        piece,dest = action
        x,y = piece
        x_dest, y_dest = dest
        dir = y_dest - y, x_dest - x
        dir_index = direction_combine.index(dir)
        return (x*8+y)*8+dir_index

