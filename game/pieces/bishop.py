from pieces.piece import Piece

class Bishop(Piece):

    def __init__(self, color, position):
        super().__init__(color, position)
        self.pgn_code = 'B'
        self.img = color[0] + "b"
        self.available_moves = []

    def get_legal_moves(self, board):
        row = self.position[0]
        col = self.position[1]
        axes = []
        board_size = 8

        axis1 = [[row + i, col + i] for i in range(1, board_size) if 0 <= row + i < board_size and 0 <= col + i < board_size]
        axes.append(sorted(axis1, key = lambda x: abs(x[0] - row) + abs(x[1] - col)))
        
        axis2 = [[row - i, col + i] for i in range(1, board_size) if 0 <= row - i < board_size and 0 <= col + i < board_size]
        axes.append(sorted(axis2, key = lambda x: abs(x[0] - row) + abs(x[1] - col)))
        
        axis3 = [[row + i, col - i] for i in range(1, board_size) if 0 <= row + i < board_size and 0 <= col - i < board_size]
        axes.append(sorted(axis3, key = lambda x: abs(x[0] - row) + abs(x[1] - col)))
        
        axis4 = [[row - i, col - i] for i in range(1, board_size) if 0 <= row - i < board_size and 0 <= col - i < board_size]
        axes.append(sorted(axis4, key = lambda x: abs(x[0] - row) + abs(x[1] - col)))

        legal_moves = []
        for axis in axes:
            for move in axis:
                if self.empty_or_can_eat(move[0], move[1], board.fields) and not board.is_king_in_check(self.position, move):
                    #print(move)
                    legal_moves.append(move)
                if board.fields[move[0]][move[1]] is not None:
                    break  # Stop further moves in this direction if a piece is encountered
        return legal_moves
    
    def get_attack_squares(self, fields):
        row = self.position[0]
        col = self.position[1]
        axes = []
        board_size = 8

        axis1 = [[row + i, col + i] for i in range(1, board_size) if 0 <= row + i < board_size and 0 <= col + i < board_size]
        axes.append(sorted(axis1, key = lambda x: abs(x[0] - row) + abs(x[1] - col)))
        
        axis2 = [[row - i, col + i] for i in range(1, board_size) if 0 <= row - i < board_size and 0 <= col + i < board_size]
        axes.append(sorted(axis2, key = lambda x: abs(x[0] - row) + abs(x[1] - col)))
        
        axis3 = [[row + i, col - i] for i in range(1, board_size) if 0 <= row + i < board_size and 0 <= col - i < board_size]
        axes.append(sorted(axis3, key = lambda x: abs(x[0] - row) + abs(x[1] - col)))
        
        axis4 = [[row - i, col - i] for i in range(1, board_size) if 0 <= row - i < board_size and 0 <= col - i < board_size]
        axes.append(sorted(axis4, key = lambda x: abs(x[0] - row) + abs(x[1] - col)))

        attack_squares = []
        for axis in axes:
            for move in axis:
                attack_squares.append(move)
                if fields[move[0]][move[1]] is not None:
                    break  # Stop further moves in this direction if a piece is encountered
        
        return attack_squares

        
# b = Bishop("white", [3,3])
# print(b.available_moves)