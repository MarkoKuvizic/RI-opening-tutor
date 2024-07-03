import pygame
import sys
from game.images import PIECES
from game.board import Board
from game.pieces import bishop, king, knight, pawn, rook, queen, piece
from movePredictor import movePredictorCnn
from movePredictor import gameProcessor
import torch
import numpy as np

# Initialize Pygame
pygame.init()
labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
# Constants
TEXT_WIDTH = 300
WIDTH, HEIGHT = 800 + 300, 800  # Dimensions of the window
ROWS, COLS = 8, 8  # Number of rows and columns
SQUARE_SIZE = 800 // COLS  # Size of each square

# Colors
WHITE = (0, 0, 255)
BLACK = (255, 255, 0)
HIGHLIGHT = (255, 0, 0)  # Color for highlighting selected square
DARK_BROWN = (101, 67, 33)
LIGHT_BROWN = (181, 101, 29)

pygame.font.init()
FONT_SIZE = 30
font = pygame.font.SysFont(None, FONT_SIZE)

model = movePredictorCnn.MoveCNN()
model.load_state_dict(torch.load('move_prediction_model2.pth'))


# Set up the display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Board")

def draw_text(win, text_list):

    # Starting position for the text
    x = 800 + 10
    y = 10
    for text in text_list:
        text_surface = font.render(text, True, BLACK)
        win.blit(text_surface, (x, y))
        y += FONT_SIZE + 10  # Move to the next line
def get_predictions(board: Board, N = 3):
    state = board.make_matrix()
    state = np.array(state).reshape(1, 1, 64)
    state = torch.tensor(state, dtype=torch.float32)
    confidences = model(state[0])
    confidences = confidences.view(8, 8).tolist()
    elements = []
    for row_index, row in enumerate(confidences):
        for col_index, element in enumerate(row):
            elements.append({'x' : row_index, 'y' : col_index, 'confidence' : element})
    elements = sorted(elements, key=lambda x: x['confidence'], reverse=True)
    moves = []
    print(elements)
    for element in elements:
        piece = board.fields[element["x"]][element["y"]]
        if not piece or len(piece.get_legal_moves(board.fields)) == 0 or piece.color != board.player:
            continue
        for (dX, dY) in piece.get_legal_moves(board.fields):
            
            moves.append({
                'x' : dX,
                'y' : dY,
                'confidence' : element['confidence'] * -confidences[dX][dY],
                'pgn' : piece.pgn_code
            })
    moves = sorted(moves, key=lambda x: x['confidence'], reverse=True)
    return moves[:N]
def draw_board(win):
    win.fill(WHITE)  # Fill the window with white to start with a blank canvas
    for row in range(ROWS):
        for col in range(COLS):
            if (row + col) % 2 == 0:
                color = LIGHT_BROWN
            else:
                color = DARK_BROWN
            pygame.draw.rect(win, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
def draw_pieces(win, board):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board.fields[row][col]
            if piece != None:
                win.blit(PIECES[piece.img], (col * SQUARE_SIZE, row * SQUARE_SIZE))
def get_square_under_mouse():
    mouse_pos = pygame.mouse.get_pos()
    x, y = mouse_pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():


    board = Board()
    board.setup()
    global selected_piece
    selected_piece = None
    possible_moves = []
    for key in PIECES:
        PIECES[key] = pygame.transform.scale(PIECES[key], (SQUARE_SIZE, SQUARE_SIZE))

    clock = pygame.time.Clock()
    run = True
    checkmate = False
    predictions = get_predictions(board)
        
    text = []
        
    for p in predictions:
        text.append(f"{p['pgn']} {labels[p['y']]}{8 - p['x']}  confidence: {p['confidence']:.6f}")
    while run:
        clock.tick(60)  # Limit the frame rate to 60 frames per second
        
        

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and not checkmate:
                row, col = get_square_under_mouse()
                if selected_piece:
                   
                    # Move the piece to the new location
                    if [row, col] in possible_moves:
                        checkmate = board.execute_move(selected_piece, [row, col])
                        selected_piece = None
                    else:
                        if board.fields[row][col] and board.fields[row][col].color == board.player:
                            selected_piece = [row, col]
                    predictions = get_predictions(board)
        
                    text = []
                    for p in predictions:
                        text.append(f"{p['pgn']} {labels[p['y']]}{8 - p['x']}  confidence: {p['confidence']:.6f}")
                else:
                    # Select the piece
                    if board.fields[row][col] and board.fields[row][col].color == board.player:
                        selected_piece = [row, col]
                    
        draw_board(WIN)
        draw_pieces(WIN, board)

        draw_text(WIN, text)

        if selected_piece:
            # Highlight the selected piece
            row, col = selected_piece
            #pygame.draw.rect(WIN, HIGHLIGHT, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
            piece = board.fields[selected_piece[0]][selected_piece[1]]
            possible_moves = []
            if piece:
                possible_moves = piece.get_legal_moves(board.fields)
            
            for move in possible_moves:
                [r, c] = move
                pygame.draw.rect(WIN, HIGHLIGHT, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

        pygame.display.flip()  # Update the display

        if checkmate:
            print("Checkmate! Game over.")
            run = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()