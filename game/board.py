from game.pieces import rook, king, pawn, knight, bishop, queen
from typing import List

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
        self.fields[7][3] = queen.Queen("white", [7, 3])
        
        self.fields[0][4] = king.King("black", [0, 4])
        self.fields[7][4] = king.King("white", [7, 4])
        
        self.fields[1] = [pawn.Pawn("black", [1, j]) for j in range(8)]
        self.fields[6] = [pawn.Pawn("white", [6, j]) for j in range(8)]
            
    def execute_move(self, position, move):
        # print("MILICA")
        piece = self.fields[position[0]][position[1]]


    def print_board(self):
        for row in self.fields:
            print(row)
    def execute_move(self, position, move, en_passant = False):
        piece = self.fields[position[0]][position[1]] 

        # Check if the move is castling
        if isinstance(piece, king.King) and abs(move[1] - position[1]) == 2:
            # King-side castling
            if move[1] > position[1]:
                rook_position = (position[0], position[1] + 3)
                new_rook_position = (position[0], position[1] + 1)
            # Queen-side castling
            else:
                rook_position = (position[0], position[1] - 4)
                new_rook_position = (position[0], position[1] - 1)
            
            castle_rook = self.fields[rook_position[0]][rook_position[1]]
            self.fields[rook_position[0]][rook_position[1]] = None
            self.fields[new_rook_position[0]][new_rook_position[1]] = castle_rook
            castle_rook.position = new_rook_position

        self.reset_en_passant()
        # We need to check whether it's en-passant before we change the position
        en_passant = isinstance(piece, pawn.Pawn) and piece.is_en_passant_move(self.fields, move)

        # Execute the move
        piece.position = move
        self.fields[position[0]][position[1]] = None
        self.fields[move[0]][move[1]] = piece

        if (en_passant):
            self.execute_en_passant(move) # dodatno obrisi piona iza ovoga

        if isinstance(piece, pawn.Pawn):
            if abs(move[0] - position[0]) > 1:
                piece.en_passantable = True
            else:
                piece.en_passantable = False

        if isinstance(piece, king.King) or isinstance(piece, rook.Rook):
            piece.has_moved = True
        
        self.change_player()

    def execute_en_passant(self, move):
        direction = -1 if self.player == "white" else 1
        self.fields[move[0] - direction][move[1]] = None

    def reset_en_passant(self):
        for row in self.fields:
            for piece in row:
                if isinstance(piece, pawn.Pawn):
                    piece.en_passantable = False

    def is_king_in_check(self, position, move):

        # Simulate the move
        original_piece = self.fields[position[0]][position[1]]
        original_piece.position = move
        self.fields[position[0]][position[1]] = None
        destination_before_move = self.fields[move[0]][move[1]]
        self.fields[move[0]][move[1]] = original_piece

        # Find the position of the king of the specified color
        king_position = None
        for row in range(8):
            for col in range(8):
                piece = self.fields[row][col]
                if isinstance(piece, king.King) and piece.color == self.player:
                    king_position = [row, col]
                    break
            if king_position:
                break
        
        if not king_position:
            return False  # King of the specified color not found (should not happen in a valid game)

        # Check if any opponent's pieces have legal moves that attack the king
        opponent_color = "white" if self.player == "black" else "black"
        for row in range(8):
            for col in range(8):
                piece = self.fields[row][col]
                if piece and piece.color == opponent_color:
                    attack_squares = piece.get_attack_squares(self.fields) # to avoid infine loop by calling get_legal_moves
                    if king_position in attack_squares:
                        # Revert the move
                        original_piece.position = [position[0], position[1]]
                        self.fields[position[0]][position[1]] = original_piece
                        self.fields[move[0]][move[1]] = destination_before_move
                        return True
        
        # Revert the move
        original_piece.position = [position[0], position[1]]
        self.fields[position[0]][position[1]] = original_piece
        self.fields[move[0]][move[1]] = destination_before_move
        return False
    
    def is_king_in_check_right_now(self):
        # Find the position of the king of the specified color
        king_position = None
        for row in range(8):
            for col in range(8):
                piece = self.fields[row][col]
                if isinstance(piece, king.King) and piece.color == self.player:
                    king_position = [row, col]
                    break
            if king_position:
                break
        
        if not king_position:
            return False  # King of the specified color not found (should not happen in a valid game)

        # Check if any opponent's pieces have legal moves that attack the king
        opponent_color = "white" if self.player == "black" else "black"
        for row in range(8):
            for col in range(8):
                piece = self.fields[row][col]
                if piece and piece.color == opponent_color:
                    attack_squares = piece.get_attack_squares(self.fields) # to avoid infine loop by calling get_legal_moves
                    if king_position in attack_squares:
                        return True
                    
        return False
    
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

        if '=' in move:
            return None, None

        if move[-1] in '+#' and move[-2] != 'O':
            move_cords = [row_dict[move[-2]], col_dict[move[-3]]]
            move = move[0:-1]

        elif 'O' not in move:
            move_cords = [row_dict[move[-1]], col_dict[move[-2]]]

        if move[0] not in 'NBRQKO':
            piece = self.get_pawn(move, move_cords)

        elif move[0] in 'KO': # za rokade isto kralj
            piece = self.get_king()
            if move.startswith('O-O-O') : move_cords = [piece.position[0], piece.position[1] - 2]
            elif move.startswith('O-O'): move_cords = [piece.position[0], piece.position[1] + 2]

        else:
            piece = self.get_piece(move, move_cords)

        return piece, move_cords
                
    def get_pawn(self, move, move_cords):
        if 'x' not in move:
            for row in range(8):
                for col in range(8):
                    piece = self.fields[row][col]
                    if piece and piece.color == self.player and isinstance(piece, pawn.Pawn) and move_cords in piece.get_legal_moves(self):
                        return piece
        else:
            col_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
            col = col_dict[move[0]]
            for row in range(8):
                piece = self.fields[row][col]
                if piece and piece.color == self.player and isinstance(piece, pawn.Pawn) and move_cords in piece.get_legal_moves(self):
                    return piece
            
    def get_piece(self, move, move_cords):
        col_dict = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
        row_dict = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
        piece_dict = {'N': knight.Knight, 'B': bishop.Bishop, 'R': rook.Rook, 'Q': queen.Queen}

        def is_valid_piece(piece):
            return piece and piece.color == self.player and isinstance(piece, piece_dict[move[0]]) and move_cords in piece.get_legal_moves(self)

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

