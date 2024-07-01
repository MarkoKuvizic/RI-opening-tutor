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

def parse_pgn(pgn):
    moves = []
    for line in pgn.split('\n'):
        if not line.strip().startswith('['):
            moves.extend(line.split(' '))
    moves = [move for move in moves if move and not move[0].isdigit() and not move.endswith('.')]
    return moves

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

    # PGN string (example)
    pgn = """
            1. e4 d5 2. Qf3 dxe4 3. Qxe4 Nf6 4. Qe5 e6 5. Bb5+ Bd7 6. Bxd7+ Qxd7 7. c4 Nc6 8. Qb5 O-O-O 9. d4 a6 10. Qb3 Nxd4 11. Qc3 Ne4 12. Qe3 Nc2+ 13. Ke2 Qd1# 0-1

            [Event "Rated Blitz game"]
            [Site "https://lichess.org/pjIgfKFJ"]
            [White "BlackBranca"]
            [Black "HardwellOfKing"]
            [Result "1-0"]
            [UTCDate "2015.12.31"]
            [UTCTime "23:01:53"]
            [WhiteElo "1817"]
            [BlackElo "1445"]
            [WhiteRatingDiff "+9"]
            [BlackRatingDiff "-11"]
            [ECO "B32"]
            [Opening "Sicilian Defense: Franco-Sicilian Variation"]
            [TimeControl "180+2"]
            [Termination "Normal"]
            """
    
    pgn2 = """
            1. e4 c5 2. g3 Nc6 3. Bg2 d6 4. c3 g6 5. d3 Bg7 6. Be3 Nf6 7. Qd2 Ng4 8. Bf4 h6 9. h3 Nf6 10. Nf3 g5 11. Be3 Be6 12. Na3 a6 13. Rb1 Qa5 14. c4 Qxd2+ 15. Bxd2 Nd7 16. O-O Nde5 17. Ne1 Nb4 18. Bxb4 cxb4 19. Nac2 Nxc4 20. dxc4 Bxc4 21. e5 Bxe5 22. Bxb7 Rb8 23. Bc6+ Kd8 24. f4 gxf4 25. gxf4 Rg8+ 26. Kh1 Bxf1 27. fxe5 dxe5 28. Kh2 Kc7 29. Be4 Rgd8 30. Ne3 Bb5 31. Nf3 Bd3 32. Rc1+ Kb6 33. Nd5+ Rxd5 34. Bxd5 e6 35. Nxe5 Rd8 36. Bg2 Bb5 37. Nxf7 Rd2 38. Nxh6 Rxb2 39. Ra1 Bc6 40. Rg1 Rxa2 41. Kg3 Rxg2+ 42. Rxg2 Bxg2 43. Kxg2 b3 44. Ng4 b2 45. Ne3 b1=Q 46. h4 Qe4+ 47. Kf2 Qxh4+ 48. Ke2 Qe4 49. Kd2 Kc5 50. Nc2 a5 51. Ne1 Kc4 52. Kc1 Qxe1+ 0-1

            [Event "Rated Blitz game"]
            [Site "https://lichess.org/XuoITSbx"]
            [White "Taiane"]
            [Black "javoaussin"]
            [Result "0-1"]
            [UTCDate "2015.12.31"]
            [UTCTime "23:01:49"]
            [WhiteElo "1899"]
            [BlackElo "1788"]
            [WhiteRatingDiff "-17"]
            [BlackRatingDiff "+22"]
            [ECO "B09"]
            [Opening "Pirc Defense: Austrian Attack #2"]
            [TimeControl "180+2"]
            [Termination "Time forfeit"]
            """

    moves = parse_pgn(pgn)
    move_delay = 500  # milliseconds between moves
    matrices = []
    # print(moves)
    # s = input()

    while run:
        clock.tick(60)  # Limit the frame rate to 60 frames per second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # if event.type == pygame.MOUSEBUTTONDOWN:
            #     row, col = get_square_under_mouse()
            #     if selected_piece:
            #         # Move the piece to the new location
            #         if [row, col] in possible_moves:
            #             board.execute_move(selected_piece, [row, col])
            #         else:
            #             if board.fields[row][col] and board.fields[row][col].color == board.player:
            #                 selected_piece = [row, col]
            #     else:
            #         # Select the piece
            #         if board.fields[row][col] and board.fields[row][col].color == board.player:
            #             selected_piece = [row, col]

        for move in moves:
            matrix = board.make_matrix()
            matrices.append(matrix)
            draw_board(WIN)
            draw_pieces(WIN, board)
            pygame.display.flip()  # Update the display
            selected_piece, move_coords = board.get_piece_and_move(move)
            possible_moves = selected_piece.get_legal_moves(board.fields)
            if move_coords in possible_moves:
                checkmate = board.execute_move(selected_piece.position, move_coords)

            pygame.time.wait(move_delay)

            # if event.type == pygame.MOUSEBUTTONDOWN and not checkmate:
            #     row, col = get_square_under_mouse()
            #     if selected_piece:
            #         # Move the piece to the new location
            #         if [row, col] in possible_moves:
            #             checkmate = board.execute_move(selected_piece, [row, col])
            #             selected_piece = None
            #         else:
            #             if board.fields[row][col] and board.fields[row][col].color == board.player:
            #                 selected_piece = [row, col]
            #     else:
            #         # Select the piece
            #         if board.fields[row][col] and board.fields[row][col].color == board.player:
            #             selected_piece = [row, col]

        # if selected_piece:
        #     # Highlight the selected piece
        #     row, col = selected_piece
        #     #pygame.draw.rect(WIN, HIGHLIGHT, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
        #     piece = board.fields[selected_piece[0]][selected_piece[1]]
        #     possible_moves = []
        #     if piece:
        #         possible_moves = piece.get_legal_moves(board.fields)
            
        #     for move in possible_moves:
        #         [r, c] = move
        #         pygame.draw.rect(WIN, HIGHLIGHT, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)


        # if selected_piece:
        #     # Highlight the selected piece
        #     row, col = selected_piece
        #     pygame.draw.rect(WIN, HIGHLIGHT, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
        #     piece = board.fields[selected_piece[0]][selected_piece[1]]
        #     possible_moves = []
        #     if piece:
        #         possible_moves = piece.get_legal_moves(board.fields)
            
        #     for move in possible_moves:
        #         [r, c] = move
        #         pygame.draw.rect(WIN, HIGHLIGHT, (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)


        pygame.display.flip()  # Update the display

        ind = 0
        for matrix in matrices:
            ind+=1
            print("MATRIX " + str(ind))
            for row in matrix:
                print(row)

        if checkmate:
            print("Checkmate! Game over.")
            run = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
