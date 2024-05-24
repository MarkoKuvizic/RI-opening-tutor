from pieces.piece import Piece
        
class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.pgn_code = ''  # Pawns do not have a letter in PGN notation
