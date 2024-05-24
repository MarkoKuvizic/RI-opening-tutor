from pieces.piece import Piece
from game.board import Board
class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.pgn_code = 'K'
        self.available_moves = [[-1,-1], [-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
        
    def get_legal_moves(self, board):
        for move in self.available_moves:
            future_position = self.position[0] + move[0]
            
    def is_in_check_from(self, piece: Piece, board: Board):
        if self.position in piece.get_check_moves(board):
            return True
    def move_checks_from(self, move, board: Board, piece:Piece):
        if move in piece.get_check_moves(board):
            return True