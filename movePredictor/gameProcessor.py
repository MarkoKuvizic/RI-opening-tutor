from torch.utils.data import Dataset
from game.board import Board
from pprint import pprint
from collections import defaultdict
import torch
import numpy as np
from preprocessor.game_processor import GameProcessor

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
        board_matrices.append([x for xs in matrix for x in xs])

    # Crop or pad board_matrices to fixed size
    #board_matrices = board_matrices[:64 * 2 * max_moves]  # Crop or pad as necessary
    #board_matrices += [0.0] * (64 * 2 * max_moves - len(board_matrices))  # Pad with zeros if necessary

    return board_matrices

class ChessDataset(Dataset):
    def __init__(self, games, max_moves = 10):
        self.games = games
        self.max_moves = max_moves
        self.board_states = []
        self.size = 0
        for game in games:
            try:
                self.flatten(game)
            except:
                pass
        self.size = len(self.board_states)
        #self.board_states = torch.tensor(self.board_states, dtype=torch.float32).view(-1, 1, 64)
        self.board_states = np.array(self.board_states).reshape(len(self.board_states), 1, 64)
        self.board_states = torch.tensor(self.board_states, dtype=torch.float32)
       
    def __len__(self):
        return self.size
    
    def __getitem__(self, idx):
        return self.board_states[idx]

    def flatten(self, game):
        pgn = game['pgn']
        states = pgn_to_matrices(pgn, self.max_moves)
        
        self.board_states.extend(states)
class ConfidenceDataset(Dataset):
    def __init__(self, games, max_moves = 10):
        self.games = games
        self.max_moves = max_moves
        self.board_states = []
        self.size = 0

        for game in games:
            try:
                self.flatten(game)
            except:
                pass
        self.size = len(self.board_states)
        self.board_states = np.array(self.board_states).reshape(len(self.board_states), 64)
        self.board_states = torch.tensor(self.board_states, dtype=torch.float32)
        
        
        

    def __len__(self):
        return self.size
    
    def __getitem__(self, idx):
        
        return self.board_states[idx]

    def flatten(self, game):
        pgn = game['pgn']
        states = pgn_to_matrices(pgn, self.max_moves)
        
        for i in range(len(states)):
            try:
                states[i] = [a_i + b_i for a_i, b_i in zip(states[i], states[i+1])]

            except Exception as e:
                print(e)
                break
        self.board_states.extend(states)
        
def test():
    torch.set_printoptions(profile="default", edgeitems=10, linewidth=1000)

    processor = GameProcessor()
    with open('D:\Marko\Downloads\lichess_db_standard_rated_2016-01.pgn/lichess_db_standard_rated_2016-01.pgn', 'r') as file:
        for i in range(10000):
            processor.read_until_string('Event', file)
    processor.filter_games()
    processor.separate_game_into_positions()
    #pprint(processor.games)
    #set = ChessDataset(processor.games)
    #pprint(set[0])
    confidences = ConfidenceDataset(processor.games)

