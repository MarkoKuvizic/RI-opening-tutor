from pieces.piece import Piece
class King(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.pgn_code = 'K'
        self.available_moves = [[-1,-1], [-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]

    def get_legal_moves(self, board):
        for move in self.available_moves:
            future_position = self.position[0] + move[0]
        