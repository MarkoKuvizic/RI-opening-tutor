from pieces import rook, king, pawn, knight, bishop, queen
class Board():
    def __init__(self):
        self.fields = [[None for _ in range(8)] for _ in range(8)]  
        self.player = "white"
    def setup(self):
        self.fields[0][0] = rook.Rook("black", [0, 0])
        self.fields[0][7] = rook.Rook("black", [0, 7])
        self.fields[7][0] = rook.Rook("white", [7, 0])
        self.fields[7][7] = rook.Rook("white", [7, 7])
        
        self.fields[0][1] = knight.Knight("black", [0, 1])
        self.fields[0][6] = knight.Knight("black", [0, 6])
        self.fields[7][1] = knight.Knight("white", [7, 1])
        self.fields[7][6] = knight.Knight("white", [7, 6])
        
        self.fields[0][2] = bishop.Bishop("black", [0, 2])
        self.fields[0][5] = bishop.Bishop("black", [0, 5])
        self.fields[7][2] = bishop.Bishop("white", [7, 2])
        self.fields[7][5] = bishop.Bishop("white", [7, 5])
        
        self.fields[0][3] = queen.Queen("black", [0, 3])
        self.fields[7][4] = queen.Queen("white", [7, 4])
        
        self.fields[0][4] = king.King("black", [0, 4])
        self.fields[7][3] = king.King("white", [7, 3])
        
        self.fields[1] = [pawn.Pawn("black", [1, j]) for j in range(8)]
        self.fields[6] = [pawn.Pawn("white", [6, j]) for j in range(8)]

        pass
    def print_board(self):
        for row in self.fields:
            print(row)
    def execute_move(self, position, move, en_passant = False):
        piece = self.fields[position[0]][position[1]] 
        self.fields[position[0]][position[1]] = None
        self.fields[move[0]][move[1]] = piece
        if (en_passant):
            self.execute_en_passant(move)
        if piece is pawn.Pawn:
            if abs(move[0] - position[0]) > 1:
                piece.en_passantable = True
            else:
                piece.en_passantable = False
    def execute_en_passant(self, move):
        direction = 1
        if self.player == "white":
            direction = -1
        self.fields[move[0] - direction][move[1]] = None
    def change_player(self):
        if self.player == "white":
            self.player = "black"
            return
        self.player = "white"