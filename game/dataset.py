import torch
from torch.utils.data import Dataset
from board import Board
from pprint import pprint
from collections import defaultdict

from game_processor import GameProcessor

# Function to parse PGN and extract moves
def parse_pgn(pgn):
    moves = []
    for line in pgn.split('\n'):
        if not line.strip().startswith('['):
            moves.extend(line.split(' '))
    moves = [move for move in moves if move and not move[0].isdigit() and not move.endswith('.')]
    return moves

# Function to convert PGN to matrices
def pgn_to_matrices(pgn, max_moves):
    board = Board()
    board.setup()
    moves = parse_pgn(pgn)
    board_matrices = []
    for i, move in enumerate(moves):
        if i >= max_moves:
            break
        if '{' in move: 
            print("milica je super")
        selected_piece, move_coords = board.get_piece_and_move(move)
        board.execute_move(selected_piece.position, move_coords)
        matrix = board.make_matrix()
        for row in matrix:
            board_matrices.extend(row)

    # Crop or pad board_matrices to fixed size
    board_matrices = board_matrices[:64 * 2 * max_moves]  # Crop or pad as necessary
    board_matrices += [0.0] * (64 * 2 * max_moves - len(board_matrices))  # Pad with zeros if necessary

    return board_matrices

class ChessDataset(Dataset):
    def __init__(self, games, max_moves = 10):
        self.games = games
        self.max_moves = max_moves
        self.opening_to_label = self._create_opening_to_label() # da numericku vrednost svakom otvaranju, jer output cnn mora da bude numericki
    
    def _create_opening_to_label(self):
        opening_to_label = defaultdict(lambda: len(opening_to_label))  # Automatically assigns new labels
        for game in self.games:
            opening_name = game['opening']
            opening_to_label[opening_name]  # This line ensures each opening gets a unique label
        return opening_to_label

    def __len__(self):
        return len(self.games)
    
    def __getitem__(self, idx):
        game = self.games[idx]
        pgn = game['pgn']
        board_states = pgn_to_matrices(pgn, self.max_moves)
        opening_name = game['opening']
        label = self.opening_to_label[opening_name]

         # Convert board_states to a PyTorch tensor and reshape
        board_states = torch.tensor(board_states, dtype=torch.float32).view(1, 1, -1)  # Assuming input channels = 1
        
        return board_states, label
    
if __name__ == "__main__":
    processor = GameProcessor()
    with open('C:/Users/milic/Desktop/RI/biii/lichess_db_standard_rated_2016-01.pgn', 'r') as file:
        for i in range(100):
            processor.read_until_string('Event', file)
    processor.filter_games()
    processor.separate_game_into_positions()
    pprint(processor.games)

    # ds = ChessDataset(processor.games)
    # # print(ds.opening_to_label)
    # for i in range(len(ds)):
    #     board_states, label = ds[i]
    #     print(len(board_states))