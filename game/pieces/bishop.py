from pieces.piece import Piece
class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.pgn_code = 'B'
