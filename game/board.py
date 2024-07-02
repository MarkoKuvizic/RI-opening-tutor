from game.pieces import rook, king, pawn, knight, bishop, queen
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

    def print_board(self):
        for row in self.fields:
            print(row)
    def execute_move(self, position, move, en_passant = False):
        piece = self.fields[position[0]][position[1]] 
        piece.position = move
        self.fields[position[0]][position[1]] = None
        self.fields[move[0]][move[1]] = piece
        if (en_passant):
            self.execute_en_passant(move)
        if piece is pawn.Pawn:
            if abs(move[0] - position[0]) > 1:
                piece.en_passantable = True
            else:
                piece.en_passantable = False
        self.change_player()
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

    
    def get_piece_and_move(self, move):
        col_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        row_dict = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
        piece = None
        move_cords = None

        if move[-1] in '+#':
            move_cords = [row_dict[move[-2]], col_dict[move[-3]]]
            move = move[0:-1]

        elif 'O' not in move:
            move_cords = [row_dict[move[-1]], col_dict[move[-2]]]

        if move[0] not in 'NBRQKO':
            piece = self.get_pawn(move, move_cords)

        elif move[0] in 'KO': # za rokade isto kralj
            piece = self.get_king()
            if move == 'O-O': move_cords = [piece.position[0], piece.position[1] + 2]
            elif move == 'O-O-O': move_cords = [piece.position[0], piece.position[1] - 2]

        else:
            piece = self.get_piece(move, move_cords)

        return piece, move_cords
                
    def get_pawn(self, move, move_cords):
        if 'x' not in move:
            for row in range(8):
                for col in range(8):
                    piece = self.fields[row][col]
                    if piece and piece.color == self.player and isinstance(piece, pawn.Pawn) and move_cords in piece.get_legal_moves(self.fields):
                        return piece
        else:
            col_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
            col = col_dict[move[0]]
            for row in range(8):
                piece = self.fields[row][col]
                if piece and piece.color == self.player and isinstance(piece, pawn.Pawn) and move_cords in piece.get_legal_moves(self.fields):
                    return piece
            
    def get_piece(self, move, move_cords):
        col_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        row_dict = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
        piece_dict = {'N': knight.Knight, 'B': bishop.Bishop, 'R': rook.Rook, 'Q': queen.Queen}

        def is_valid_piece(piece):
            return piece and piece.color == self.player and isinstance(piece, piece_dict[move[0]]) and move_cords in piece.get_legal_moves(self.fields)

        def find_piece(move_cords, col=None, row=None):
            for r in range(8):
                for c in range(8):
                    if col is not None and c != col:
                        continue
                    if row is not None and r != row:
                        continue
                    piece = self.fields[r][c]
                    if is_valid_piece(piece):
                        return piece
            return None

        if len(move) == 3 or (len(move) == 4 and 'x' in move):
            return find_piece(move_cords)

        elif move[1] in col_dict.keys():

            if move[2] in row_dict.keys(): # ako imamo bas tacnu pocetnu lokaciju
                return find_piece(move_cords, col=col_dict[move[1]], row=row_dict[move[1]])

            return find_piece(move_cords, col=col_dict[move[1]])
                
        elif move[1] in row_dict.keys():
            return find_piece(move_cords, row=row_dict[move[1]])
    
    def get_king(self):
        for row in range(8):
            for col in range(8):
                piece = self.fields[row][col]
                if piece and piece.color == self.player and isinstance(piece, king.King):
                    return piece
    
    def make_matrix(self):
        matrix = [[0 for _ in range(8)] for _ in range(8)]
        dec_val = {
            'Pawn': 0.1,
            'Knight': 0.2,
            'Bishop': 0.3,
            'Rook': 0.4,
            'Queen': 0.5,
            'King': 0.6,
        }
        for row in range(8):
            for col in range(8):
                piece = self.fields[row][col]

                if piece == None:
                    continue

                piece_type = str(piece)
                piece_type = piece_type.split()[1]

                if piece.color == self.player:
                    matrix[row][col] = dec_val[piece_type]
                else:
                    matrix[row][col] = -dec_val[piece_type]

        return matrix
