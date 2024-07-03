from pieces.piece import Piece

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.pgn_code = 'R'
        self.img = color[0] + "r"
        self.has_moved = False
        self.available_moves = []
        
    def get_legal_moves(self, board):
        axes = []
        legal_moves = []
        
        row = self.position[0]
        col = self.position[1]
        
        axis1 = [[i, self.position[1]] for i in range(self.position[0] + 1, 8)]
        axis2 = [[i, self.position[1]] for i in range(0, self.position[0])]
        axis3 = [[self.position[0], j] for j in range(self.position[1] + 1, 8)]
        axis4 = [[self.position[0], j] for j in range(0, self.position[1])]
        
        
        axes.append(sorted(axis1, key = lambda x: abs(x[0] - row) + abs(x[1] - col)))
        axes.append(sorted(axis2, key = lambda x: abs(x[0] - row) + abs(x[1] - col)))
        axes.append(sorted(axis3, key = lambda x: abs(x[0] - row) + abs(x[1] - col)))
        axes.append(sorted(axis4, key = lambda x: abs(x[0] - row) + abs(x[1] - col)))

        for axis in axes:
            # print(axis)
            for move in axis:
                if self.empty_or_can_eat(move[0], move[1], board.fields) and not board.is_king_in_check(self.position, move):
                    legal_moves.append(move)
                if board.fields[move[0]][move[1]] is not None:
                    break  # Stop further moves in this direction if a piece is encountered
        return legal_moves
    
    def get_attack_squares(self, fields):
        axes = []
        legal_moves = []
        
        row = self.position[0]
        col = self.position[1]
        
        axis1 = [[i, self.position[1]] for i in range(self.position[0] + 1, 8)]
        axis2 = [[i, self.position[1]] for i in range(0, self.position[0])]
        axis3 = [[self.position[0], j] for j in range(self.position[1] + 1, 8)]
        axis4 = [[self.position[0], j] for j in range(0, self.position[1])]
        
        
        axes.append(sorted(axis1, key = lambda x: abs(x[0] - row) + abs(x[1] - col)))
        axes.append(sorted(axis2, key = lambda x: abs(x[0] - row) + abs(x[1] - col)))
        axes.append(sorted(axis3, key = lambda x: abs(x[0] - row) + abs(x[1] - col)))
        axes.append(sorted(axis4, key = lambda x: abs(x[0] - row) + abs(x[1] - col)))

        for axis in axes:
            # print(axis)
            for move in axis:
                legal_moves.append(move)
                if fields[move[0]][move[1]] is not None:
                    break  # Stop further moves in this direction if a piece is encountered
        return legal_moves
