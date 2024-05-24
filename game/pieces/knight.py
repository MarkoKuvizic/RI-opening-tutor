from pieces.piece import Piece

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.img = color[0] + "n"
        self.pgn_code = 'N'
        
        row = position[0]
        col = position[1]
        self.available_moves = [[row-2,col-1],[row-2,col+1],[row-1,col-2],[row-1,col+2],[row+1,col-2],[row+1,col+2],[row+2,col-1],[row+2,col+1]]
        