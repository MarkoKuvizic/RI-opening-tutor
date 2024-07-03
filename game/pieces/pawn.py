from game.pieces.piece import Piece
from typing import List, Optional

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.img = color[0] + "p"
        self.pgn_code = ''
        self.direction = -1 if color == 'white' else 1
        self.en_passantable = False

    def get_legal_moves(self, fields: List):
        legal_moves = []
        row, col = self.position
        
        # Standard one square forward move
        forward_row = row + self.direction
        if 0 <= forward_row < 8 and fields[forward_row][col] is None:
            legal_moves.append([forward_row, col])
            
            # Two squares forward move if on the starting row
            starting_row = 6 if self.color == 'white' else 1
            if row == starting_row:
                two_squares_forward_row = row + 2 * self.direction
                if 0 <= two_squares_forward_row < 8 and fields[two_squares_forward_row][col] is None:
                    legal_moves.append([two_squares_forward_row, col])
        
        # Capture moves (diagonal forward)
        for dc in [-1, 1]:
            capture_row = row + self.direction
            capture_col = col + dc
            if 0 <= capture_row < 8 and 0 <= capture_col < 8:
                if fields[capture_row][capture_col] is not None and fields[capture_row][capture_col].color != self.color:
                    legal_moves.append([capture_row, capture_col])

        # Check is en-passant possible
        en_passant_position = self.get_en_passant(fields)
        if en_passant_position is not None:
            legal_moves.append(en_passant_position)

        return legal_moves
    
    def get_en_passant(self, fields):
        positions = []
        left_col = self.position[1] - 1
        right_col = self.position[1] + 1
        if 0 <= left_col < 8: positions.append([self.position[0], left_col])
        if 0 <= right_col < 8: positions.append([self.position[0], right_col])        

        for position in positions:
            p = fields[position[0]][position[1]]
            if isinstance(p, Pawn) and p.en_passantable:
                return [position[0] + self.direction, position[1]]
    
    # Used in board.py excecute_move to determine whether the move is en-passant
    def is_en_passant_move(self, fields: List[Optional[Piece]], move: List[int]) -> bool:
        if self.position[1] != move[1] and fields[move[0]][move[1]] is None:
            return True
        return False