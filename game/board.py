from pieces import rook, king, pawn, knight, bishop, queen
class Board():
    def __init__(self):
        self.fields = [[None for _ in range(8)] for _ in range(8)]  
    def setup(self):
        self.fields[0][0] = rook.Rook("black")
        self.fields[0][7] = rook.Rook("black")
        self.fields[7][0] = rook.Rook("white")
        self.fields[7][7] = rook.Rook("white")
        
        self.fields[0][1] = knight.Knight("black")
        self.fields[0][6] = knight.Knight("black")
        self.fields[7][1] = knight.Knight("white")
        self.fields[7][6] = knight.Knight("white")
        
        self.fields[0][2] = bishop.Bishop("black")
        self.fields[0][5] = bishop.Bishop("black")
        self.fields[7][2] = bishop.Bishop("white")
        self.fields[7][5] = bishop.Bishop("white")
        
        self.fields[0][3] = queen.Queen("black")
        self.fields[7][4] = queen.Queen("white")
        
        self.fields[0][4] = king.King("black")
        self.fields[7][3] = king.King("white")
        
        self.fields[1] = [pawn.Pawn("black") for _ in range(8)]
        self.fields[6] = [pawn.Pawn("white") for _ in range(8)]

        pass
    def print_board(self):
        for row in self.fields:
            print(row)

b = Board()
b.setup()
b.print_board()