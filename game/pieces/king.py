from pieces.piece import Piece

class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.pgn_code = 'K'
        self.img = color[0] + "k"
        
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
                if self.empty_or_can_eat(new_row, new_col, board) and not self.move_checks((new_row, new_col), board):
                    legal_moves.append([new_row, new_col])

        return legal_moves
        

            
    def is_in_check_from(self, piece: Piece, board):
        if self.position in piece.get_check_moves(board):
            return True
        
    def move_checks_from(self, move, board, piece:Piece):
        if move in piece.get_check_moves(board):
            return True
        
    def move_checks(self, move, fields):
        for row in fields:
            for pos in row:
                if pos and pos.color != self.color:
                    if self.move_checks_from(move, fields, pos):
                        return True
        return False