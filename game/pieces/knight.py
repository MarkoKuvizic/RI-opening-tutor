from pieces.piece import Piece

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.pgn_code = 'N'
