class Piece():
    def __init__(self, color, position):
        self.color = color
        self.pgn_code = ''
        self.position = position
    def get_legal_moves(self, board):
        return []
    def get_check_moves(self, board):
        return []
    def __str__(self):
        return f"{self.color} {self.__class__.__name__} ({self.pgn_code})"
    
    def __repr__(self):
        return f"{self.color} {self.__class__.__name__} ({self.pgn_code})"