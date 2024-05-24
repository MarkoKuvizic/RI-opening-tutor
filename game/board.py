from pieces import rook, king, pawn, knight, bishop, queen
class Board():
    def __init__(self):
        self.fields = [[None for _ in range(8)] for _ in range(8)]  
    def setup(self):
        self.fields[0][0] = rook.Rook("white")
        self.fields[0][7] = rook.Rook("white")
        self.fields[7][0] = rook.Rook("black")
        self.fields[7][7] = rook.Rook("black")
        
        self.fields[]
        pass
    def print_board(self):
        for row in self.fields:
            print(row)

b = Board()
b.setup()
b.print_board()