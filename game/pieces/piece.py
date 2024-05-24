class Piece():
    def __init__(self, color, position):
        self.color = color
        self.pgn_code = ''

        self.position = position
    
    def get_check_moves(self, board):
        return []

    def get_legal_moves(self, board):
        legal_moves = []
        for move in self.available_moves:
            future_row = move[0]
            future_col = move[1]
            if self.inside_board(future_row, future_col) and self.empty_or_can_eat(future_row, future_col, board):
                legal_moves.append(move)

        return legal_moves
    
    def inside_board(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8
    
    def empty_or_can_eat(self, row, col, board):
        return board[row][col] is None or board[row][col].color != self.color

    def __str__(self):
        return f"{self.color} {self.__class__.__name__} ({self.pgn_code})"
    
    def __repr__(self):
        return f"{self.color} {self.__class__.__name__} ({self.pgn_code})"