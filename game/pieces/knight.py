from game.pieces.piece import Piece
from typing import List, Optional

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.img = color[0] + "n"
        self.pgn_code = 'N'

    def get_legal_moves(self, board):
        row, col = self.position
        potential_moves = [
            [row-2, col-1], [row-2, col+1], 
            [row-1, col-2], [row-1, col+2], 
            [row+1, col-2], [row+1, col+2], 
            [row+2, col-1], [row+2, col+1]
        ]

        legal_moves = []
        for move in potential_moves:
            r, c = move
            if 0 <= r < 8 and 0 <= c < 8:  # Check if the move is within the bounds of the board
                if (board.fields[r][c] is None or board.fields[r][c].color != self.color) and not board.is_king_in_check(self.position, move):  # Check if the square is empty or contains an opponent's piece
                    legal_moves.append(move)
        
        return legal_moves
    
    def get_attack_squares(self, fields):
        row, col = self.position
        attack_squares = [
            [row-2, col-1], [row-2, col+1], 
            [row-1, col-2], [row-1, col+2], 
            [row+1, col-2], [row+1, col+2], 
            [row+2, col-1], [row+2, col+1]
        ]
        real_attack_squares = []
        for move in attack_squares:
            r, c = move
            if 0 <= r < 8 and 0 <= c < 8:
                real_attack_squares.append(move)
        
        return real_attack_squares
