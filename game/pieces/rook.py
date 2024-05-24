from pieces.piece import Piece

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.pgn_code = 'R'
        self.available_moves = []
        
        self.available_moves.extend([[i, self.position[1]] for i in range(self.position[0] + 1, 8)])
        self.available_moves.extend([[i, self.position[1]] for i in range(0, self.position[0])])
        
        self.available_moves.extend([[self.position[0], j] for j in range(self.position[1] + 1, 8)])
        self.available_moves.extend([[self.position[0], j] for j in range(0, self.position[1])])
