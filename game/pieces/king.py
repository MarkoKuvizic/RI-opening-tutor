from pieces.piece import Piece
from pieces.bishop import Bishop

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.pgn_code = 'K'
        self.img = color[0] + "k"
        self.has_moved = False
        
    def get_legal_moves(self, board):
        row, col = self.position
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),  # Vertical and horizontal
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonals
        ]
        legal_moves = []

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.empty_or_can_eat(new_row, new_col, board.fields) and not self.move_checks([new_row, new_col], board.fields):
                    legal_moves.append([new_row, new_col])

        # Castling
        if not self.has_moved:
            # King-side castling
            if self.can_castle(board.fields, row, col, row, col + 3):
                legal_moves.append([row, col + 2])
            # Queen-side castling
            if self.can_castle(board.fields, row, col, row, col - 4):
                legal_moves.append([row, col - 2])

        return legal_moves
    
    def get_attack_squares(self, fields):
        row, col = self.position
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),  # Vertical and horizontal
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonals
        ]
        legal_moves = []

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                if self.empty_or_can_eat(new_row, new_col, fields):
                    legal_moves.append([new_row, new_col])

        return legal_moves
        
    def can_castle(self, board, king_row, king_col, rook_row, rook_col):
        # Check if rook has moved
        rook = board[rook_row][rook_col]
        if not isinstance(rook, Piece) or rook.has_moved or rook.color != self.color:
            return False
        
        # Check if the path is clear and not in check
        step = 1 if rook_col > king_col else -1
        for col in range(king_col + step, rook_col, step):
            if board[king_row][col] is not None or self.move_checks([king_row, col], board):
                return False
        
        return True
        
    # def move_checks(self, move, fields):
    #     for row in fields:
    #         for pos in row:
    #             if pos and pos.color != self.color:
    #                 if self.move_checks_from(move, fields, pos):
    #                     return True
    #     return False

    def move_checks(self, kings_move, fields):
        for row in range(8):
            for col in range(8):
                piece = fields[row][col]
                if piece and piece.color != self.color:
                    attack_squares = piece.get_attack_squares(fields) # kad je drugi kralj ne mora kod njega da dodaje rokadu u legal moves jer je to kao potez unapred
                    if kings_move in attack_squares:
                        return True