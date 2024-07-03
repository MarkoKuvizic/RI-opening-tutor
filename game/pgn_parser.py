import numpy as np

class PGNParser:
    def __init__(self, pgn_file):
        self.pgn_file = pgn_file

    def parse_pgn(self):
        pgn = open(self.pgn_file)
        games = []
        while True:
            game = chess.pgn.read_game(pgn)
            if game is None:
                break
            games.append(game)
        return games

    def game_to_matrices(self, game):
        board = game.board()
        matrices = []
        for move in game.mainline_moves()[:20]:  # First 10 moves (20 ply)
            board.push(move)
            matrix = self.board_to_matrix(board)
            matrices.append(matrix)
        return matrices

    def board_to_matrix(self, board):
        matrix = np.zeros((8, 8))
        piece_map = board.piece_map()
        for square, piece in piece_map.items():
            row, col = divmod(square, 8)
            matrix[row, col] = self.piece_to_value(piece)
        return matrix

    def piece_to_value(self, piece):
        piece_values = {'P': 0.1, 'N': 0.2, 'B': 0.3, 'R': 0.4, 'Q': 0.5, 'K': 0.6}
        value = piece_values[piece.symbol().upper()]
        return value if piece.color == chess.WHITE else -value

    def extract_opening(self, game):
        return game.headers["Opening"]
