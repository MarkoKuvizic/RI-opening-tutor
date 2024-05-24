class Piece():
    def __init__(self, color):
        self.color = color
        self.pgn_code = ''
        self.position = []

    def __str__(self):
        return f"{self.color} {self.__class__.__name__} ({self.pgn_code})"
    
    def __repr__(self):
        return f"{self.color} {self.__class__.__name__} ({self.pgn_code})"