from pieces.piece import Piece
class Queen(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.pgn_code = 'Q'
        self.img = color[0] + "q"
        board_size = 8
        row = self.position[0]
        col = self.position[1]
        self.available_moves = [[row + i, col + i] for i in range(1, board_size) if 0 <= row + i < board_size and 0 <= col + i < board_size] + \
            [[row - i, col + i] for i in range(1, board_size) if 0 <= row - i < board_size and 0 <= col + i < board_size] + \
            [[row + i, col - i] for i in range(1, board_size) if 0 <= row + i < board_size and 0 <= col - i < board_size] + \
            [[row - i, col - i] for i in range(1, board_size) if 0 <= row - i < board_size and 0 <= col - i < board_size]
            
        self.available_moves.extend([[i, self.position[1]] for i in range(self.position[0] + 1, 8)])
        self.available_moves.extend([[i, self.position[1]] for i in range(0, self.position[0])])
        
        self.available_moves.extend([[self.position[0], j] for j in range(self.position[1] + 1, 8)])
        self.available_moves.extend([[self.position[0], j] for j in range(0, self.position[1])])