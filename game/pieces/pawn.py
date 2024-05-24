from pieces.piece import Piece
        
class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.pgn_code = ''  # Pawns do not have a letter in PGN notation
        self.direction = -1 if color == 'white' else 1

    def get_legal_moves(self, board):
        legal_moves = []
        row, col = self.position
        
        # Standard one square forward move
        forward_row = row + self.direction
        if 0 <= forward_row < 8 and board[forward_row, col] is None:
            legal_moves.append([forward_row, 0])
            
            # Two squares forward move if on the starting row
            starting_row = 6 if self.color == 'white' else 1
            if row == starting_row:
                two_squares_forward_row = row + 2 * self.direction
                if 0 <= two_squares_forward_row < 8 and board[two_squares_forward_row, col] is None:
                    legal_moves.append([two_squares_forward_row, 0])

        # Capture moves (diagonal forward)
        for dc in [-1, 1]:
            capture_row = row + self.direction
            capture_col = col + dc
            if 0 <= capture_row < 8 and 0 <= capture_col < 8:
                if board[capture_row, capture_col] is not None and board[capture_row, capture_col].color != self.color:
                    legal_moves.append([capture_row, capture_col])

        return legal_moves
