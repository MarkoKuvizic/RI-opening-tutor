from pieces.piece import Piece
class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.img = color[0] + "p"
        self.pgn_code = ''  # Pawns do not have a letter in PGN notation
        self.direction = -1 if color == 'white' else 1
        self.en_passantable = False

    def get_legal_moves(self, board):
        legal_moves = []
        row, col = self.position
        
        # Standard one square forward move
        forward_row = row + self.direction
        if 0 <= forward_row < 8 and board[forward_row][col] is None:
            legal_moves.append([forward_row, col])
            
            # Two squares forward move if on the starting row
            starting_row = 6 if self.color == 'white' else 1
            if row == starting_row:
                two_squares_forward_row = row + 2 * self.direction
                if 0 <= two_squares_forward_row < 8 and board[two_squares_forward_row][col] is None:
                    legal_moves.append([two_squares_forward_row, col])

        # Capture moves (diagonal forward)
        for dc in [-1, 1]:
            capture_row = row + self.direction
            capture_col = col + dc
            if 0 <= capture_row < 8 and 0 <= capture_col < 8:
                if board[capture_row][capture_col] is not None and board[capture_row][capture_col].color != self.color:
                    legal_moves.append([capture_row, capture_col])

        return legal_moves
    
    def get_en_passant(self, board):
        pieces = [self.position - [0, 1], self.position + [0, 1]]
        for piece in pieces:
            p = board.fields[piece[0]][piece[1]]
            if p is Pawn and p.en_passantable:
                return piece
    