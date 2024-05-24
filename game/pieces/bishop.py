from piece import Piece
class Bishop(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.pgn_code = 'B'
        
        board_size = 8
        row = self.position[0]
        col = self.position[1]
        self.available_moves = [[row + i, col + i] for i in range(1, board_size) if 0 <= row + i < board_size and 0 <= col + i < board_size] + \
            [[row - i, col + i] for i in range(1, board_size) if 0 <= row - i < board_size and 0 <= col + i < board_size] + \
            [[row + i, col - i] for i in range(1, board_size) if 0 <= row + i < board_size and 0 <= col - i < board_size] + \
            [[row - i, col - i] for i in range(1, board_size) if 0 <= row - i < board_size and 0 <= col - i < board_size]
b = Bishop("white", [3,3])
print(b.available_moves)