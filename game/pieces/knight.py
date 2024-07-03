from game.pieces.piece import Piece
from typing import List, Optional

class Knight(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.img = color[0] + "n"
        self.pgn_code = 'N'

    def get_legal_moves(self, board: List[List[Optional[Piece]]]) -> List[List[int]]:
        row, col = self.position
        potential_moves = [
            [row-2, col-1], [row-2, col+1], 
            [row-1, col-2], [row-1, col+2], 
            [row+1, col-2], [row+1, col+2], 
            [row+2, col-1], [row+2, col+1]
        ]

        legal_moves = []
        for move in potential_moves:
            r, c = move
            if 0 <= r < 8 and 0 <= c < 8:  # Check if the move is within the bounds of the board
                if board[r][c] is None or board[r][c].color != self.color:  # Check if the square is empty or contains an opponent's piece
                    legal_moves.append(move)

        return legal_moves