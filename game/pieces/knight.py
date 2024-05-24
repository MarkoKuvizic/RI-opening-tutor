from pieces.piece import Piece

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.pgn_code = 'N'
        self.available_moves = [[-2,-1],[-2,1],[-1,-2],[-1,2],[1,-2],[1,2],[2,-1],[2,1]]