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
        # print(i, move)
        try:
            selected_piece, move_coords = board.get_piece_and_move(move)
            board.execute_move(selected_piece.position, move_coords)
            matrix = board.make_matrix()
            board_matrices.append([x for xs in matrix for x in xs])
        except:
            break
    # print(board_matrices)

    # Crop or pad board_matrices to fixed size
    # board_matrices = board_matrices[:64 * 2 * max_moves]  # Crop or pad as necessary
    # board_matrices += [0.0] * (64 * 2 * max_moves - len(board_matrices))  # Pad with zeros if necessary


    return board_matrices

class ChessDataset(Dataset):
    def __init__(self, games, openings, max_moves=10):
        self.games = games
        self.max_moves = max_moves
        self.opening_to_label = self._create_opening_to_label(openings)
        self.board_state_label_pairs = self._create_board_state_label_pairs()
    
    def _create_opening_to_label(self, openings):
        opening_dict = {}
        index = 0

        for opening in openings:
            opening_dict[opening] = index
            index += 1
            
        return opening_dict

    def _create_board_state_label_pairs(self):
        pairs = []
        for game in self.games:
            pgn = game['pgn']
            board_states = pgn_to_matrices(pgn, self.max_moves)
            label = self.opening_to_label[game['opening']]
            for board_state in board_states:
                pairs.append((board_state, label))
        
        # print(board_states[-1], game['opening'])
        return pairs

    def __len__(self):
        return len(self.board_state_label_pairs)
    
    def __getitem__(self, idx):
        board_state, label = self.board_state_label_pairs[idx]
        board_state = torch.tensor(board_state, dtype=torch.float32).view(1, 64)
        return board_state, label
    
# if __name__ == "__main__":
    # processor = GameProcessor()
    # with open('C:/Users/milic/Desktop/RI/biii/lichess_db_standard_rated_2016-01.pgn', 'r') as file:
    #     for i in range(100):
    #         processor.read_until_string('Event', file)
    # processor.filter_games()
    # processor.separate_game_into_positions()
    # pprint(processor.games)
