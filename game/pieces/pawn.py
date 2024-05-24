from pieces.piece import Piece
        
class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        self.pgn_code = ''  # Pawns do not have a letter in PGN notation
