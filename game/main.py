import pygame
import sys
from images import PIECES
from board import Board

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800  # Dimensions of the window
ROWS, COLS = 8, 8  # Number of rows and columns
SQUARE_SIZE = WIDTH // COLS  # Size of each square

# Colors
WHITE = (0, 0, 255)
BLACK = (255, 255, 0)
HIGHLIGHT = (255, 0, 0)  # Color for highlighting selected square



# Set up the display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Board")

def draw_board(win):
    win.fill(WHITE)  # Fill the window with white to start with a blank canvas
    for row in range(ROWS):
        for col in range(COLS):
            if (row + col) % 2 == 0:
                color = WHITE
            else:
                color = BLACK
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

    while run:
        clock.tick(60)  # Limit the frame rate to 60 frames per second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_square_under_mouse()
                if selected_piece:
                    # Move the piece to the new location
                    if [row, col] in possible_moves:
                        board.execute_move(selected_piece, [row, col])
                    else:
                        if board.fields[row][col] and board.fields[row][col].color == board.player:
                            selected_piece = [row, col]
                else:
                    # Select the piece
                    if board.fields[row][col] and board.fields[row][col].color == board.player:
                        selected_piece = [row, col]
                    
        draw_board(WIN)
        draw_pieces(WIN, board)

        if selected_piece:
            # Highlight the selected piece
            row, col = selected_piece
            pygame.draw.rect(WIN, HIGHLIGHT, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
            piece = board.fields[selected_piece[0]][selected_piece[1]]
            possible_moves = []
            if piece:
                possible_moves = piece.get_legal_moves(board.fields)
            
            for move in possible_moves:
                [r, c] = move
                pygame.draw.rect(WIN, HIGHLIGHT, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)


        pygame.display.flip()  # Update the display

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
