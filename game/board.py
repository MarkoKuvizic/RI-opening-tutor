from typing import List

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
        self.fields[7][3] = queen.Queen("white", [7, 3])
        
        self.fields[0][4] = king.King("black", [0, 4])
        self.fields[7][4] = king.King("white", [7, 4])
        
        self.fields[1] = [pawn.Pawn("black", [1, j]) for j in range(8)]
        self.fields[6] = [pawn.Pawn("white", [6, j]) for j in range(8)]
            
    def execute_move(self, position, move):
        print("MILICA")
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

        # Execute the move
        piece.position = move
        self.fields[position[0]][position[1]] = None
        destination_before_move = self.fields[move[0]][move[1]]
        self.fields[move[0]][move[1]] = piece

        # Check if the move puts the current player's king in check
        if self.is_king_in_check():
            # Revert the move
            piece.position = position
            self.fields[position[0]][position[1]] = piece
            self.fields[move[0]][move[1]] = destination_before_move
            return # Move would leave the king in check, so it's not allowed
        
        self.reset_en_passant()
        # We need to check whether it's en-passant before we change the position
        en_passant = isinstance(piece, pawn.Pawn) and piece.is_en_passant_move(self.fields, move)

        if (en_passant):
            self.execute_en_passant(move)

        if isinstance(piece, pawn.Pawn):
            if abs(move[0] - position[0]) > 1:
                piece.en_passantable = True
            else:
                piece.en_passantable = False

        if isinstance(piece, king.King) or isinstance(piece, rook.Rook):
            piece.has_moved = True
        
        self.change_player()

        if self.is_checkmate():
            return True
        
        return False

    def execute_en_passant(self, move):
        direction = -1 if self.player == "white" else 1
        self.fields[move[0] - direction][move[1]] = None

    def reset_en_passant(self):
        for row in self.fields:
            for piece in row:
                if isinstance(piece, pawn.Pawn):
                    piece.en_passantable = False

    def is_king_in_check(self):
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
                    legal_moves = piece.get_legal_moves(self.fields)
                    if king_position in legal_moves:
                        return True
        
        return False
    
    def is_checkmate(self):
        if not self.is_king_in_check():
            return False  # If the king is not in check, it's not checkmate

        # Check if any legal move can prevent the checkmate
        for row in range(8):
            for col in range(8):
                piece = self.fields[row][col]
                if piece and piece.color == self.player:
                    legal_moves = piece.get_legal_moves(self.fields)
                    for move in legal_moves:
                        # Simulate the move
                        original_position = piece.position
                        destination_before_move = self.fields[move[0]][move[1]]
                        self.fields[row][col] = None
                        self.fields[move[0]][move[1]] = piece
                        piece.position = move

                        if not self.is_king_in_check():
                            # Revert the move
                            piece.position = original_position
                            self.fields[row][col] = piece
                            self.fields[move[0]][move[1]] = destination_before_move
                            return False  # There is at least one legal move that prevents checkmate

                        # Revert the move
                        piece.position = original_position
                        self.fields[row][col] = piece
                        self.fields[move[0]][move[1]] = destination_before_move

        return True  # No legal moves left to prevent checkmate

    
    def change_player(self):
        if self.player == "white":
            self.player = "black"
            return
        self.player = "white"