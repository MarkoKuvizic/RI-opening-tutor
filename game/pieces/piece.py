class Piece():
    def __init__(self, color, position):
        self.color = color
        self.pgn_code = ''

        self.position = position
    
    def inside_board(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8
    
    def empty_or_can_eat(self, row, col, fields):
        return fields[row][col] is None or (fields[row][col].color != self.color)  # and board[row][col].pgn_code !="K" mislim da ne treba jer svakako neces biti u prilici da pojedes kralja jer protivnik mora da se pomeri pre tvog poteza

    def __str__(self):
        return f"{self.color} {self.__class__.__name__} ({self.pgn_code})"
    
    def __repr__(self):
        return f"{self.color} {self.__class__.__name__} ({self.pgn_code})"