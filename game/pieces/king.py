from pieces.piece import Piece
from game.board import Board
class King(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.pgn_code = 'K'

        row = self.position[0]
        col = self.position[1]
        self.available_moves = [[row-1,col-1], [row-1,col],[row-1,col+1],[row,col-1],[row,col+1],[row+1,col-1],[row+1,col],[row+1,col+1]]
        
    def get_legal_moves(self, board: Board):
        legal_moves = super.get_legal_moves()

        return [move for move in legal_moves if not self.move_checks(move, board)]

            
    def is_in_check_from(self, piece: Piece, board: Board):
        if self.position in piece.get_check_moves(board):
            return True
        
    def move_checks_from(self, move, board: Board, piece:Piece):
        if move in piece.get_check_moves(board):
            return True
    def move_checks(self, move, board: Board):
        for row in board.fields:
            for pos in row:
                if pos and pos.color != self.color:
                    if self.move_checks_from(move, board, pos):
                        return True
        return False