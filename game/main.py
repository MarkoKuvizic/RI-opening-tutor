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
DARK_BROWN = (101, 67, 33)
LIGHT_BROWN = (181, 101, 29)



# Set up the display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Board")

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
    
    pgn3 = "1. e4 d5 2. exd5 Qxd5 3. Nc3 Qa5 4. d4 Nf6 5. Ne2 Nc6 6. Bd2 Bg4 7. Ne4 Qd5 8. c3 Qxe4 9. f3 Bxf3"

    pgn4 = "1. d4 Nf6 2. c4 g6 3. Nf3 Bg7 4. Nc3 d6 5. e4 Bg4 6. Be2 e5 7. dxe5 Bxf3 8. exf6 Bxe2 9. fxg7 Bxd1 10. gxh8=Q+ Ke7 11. Bg5+ f6 12. Bxf6+ Kd7 13. Qxd8+ Kc6 14. Qe8+ Nd7 15. Qxa8 Bg4 16. Bd4 1-0"

    pgn5 = "1. e4 Nc6 2. d4 d5 3. Nc3 dxe4 4. d5 Ne5 5. Nxe4 a6 6. Bf4 Ng6 7. Bg3 f5 8. Ng5 e5 9. dxe6 Qxg5 10. Bxc7 Bxe6 11. Nf3 Qe7 12. Ba5 Bc4+ 13. Be2 Qxe2+ 14. Qxe2+ Bxe2 15. Kxe2 Be7 16. Rhe1 Nf6 17. Kf1 O-O 18. Ng5 Rac8 19. Bc3 b5 20. a3 Rfe8 21. Ne6 Nf8 22. Nd4 g6 23. Rad1 Ne4 24. Ba5 Bf6 25. f3 Nc5 26. c3 Rxe1+ 27. Rxe1 Nd3 28. Re2 Bxd4 29. cxd4 Rc1+ 30. Be1 Rxe1+ 31. Rxe1 Nxe1 32. Kxe1 Ne6 33. d5 Nf4 34. d6 Nxg2+ 35. Kf2 Nf4 36. Ke3 Ne6 37. Kd3 Kf7 38. a4 Nc5+ 39. Kd4 Nxa4 40. Kd5 Ke8 41. b3 Kd7 42. bxa4 bxa4 43. Kc4 a5 44. h4 Kxd6 45. f4 h6 46. Kd4 a3 47. Kc3 a4 0-1"

    pgn6 = '1. d4 d5 2. e4 c6 3. Nc3 dxe4 4. f3 exf3 5. Qxf3 Nf6 6. Bg5 Bg4 7. O-O-O Bxf3 8. Nxf3 e6 9. d5 cxd5 10. Bb5+ Nc6 11. Ne5 Qb6 12. Nxc6 bxc6 13. Bxf6 gxf6 14. Rhe1 cxb5 15. Nxd5 Bh6+ 16. Kb1 Qd8 17. Nxf6+ Qxf6 18. Re3 Bxe3 19. Re1 Bd2 20. Rd1 O-O 21. Rxd2 Qf1+ 22. Rd1 Qxd1# 0-1'

    pgn7 = '1. e4 e5 2. Nf3 Nc6 3. Bc4 Be7 4. O-O Nf6 5. Re1 O-O 6. d3 d6 7. Nbd2 h6 8. Nf1 Be6 9. h3 Bxc4 10. dxc4 Nd4 11. b3 Nxf3+ 12. Qxf3 Re8 13. Ng3 Nd7 14. Be3 Bg5 15. Bxg5 Qxg5 16. Nf5 Nf6 17. h4 Qg6 18. Re3 Qg4 19. Qxg4 Nxg4 20. Rg3 h5 21. f3 g6 22. Nxd6 cxd6 23. fxg4 hxg4 24. Rxg4 Re6 25. Rf1 Kg7 26. Rf3 Kh6 27. Rfg3 Rc8 28. h5 b6 29. hxg6 Rxg6 30. Rh4+ Kg7 31. Rxg6+ fxg6 32. Rg4 Rf8 33. Rg3 1-0'

    pgn8 = '1. e4 e5 2. Nf3 f6 3. Nxe5 fxe5 4. Qh5+ Ke7 5. Qxe5+ Kf7 6. Bc4+ d5 7. Bxd5+ Kg6 8. h4 h6 9. Qg3+ Kh7 10. Bc4 Bd6 11. Qd3 Qf6 12. e5+ Qg6 13. Qxg6+ Kxg6 14. exd6 cxd6 15. O-O Nf6 16. d4 Nc6 17. Bd3+ Kh5 18. g3 Nxd4 19. Be3 Nf3+ 20. Kg2 Ne5 21. Be2+ Kg6 22. f4 Neg4 23. Bd4 h5 24. c3 Re8 25. Bd3+ Bf5 26. Bb5 Be4+ 27. Kg1 Bc6 28. Bd3+ Be4 29. Bb5 Re7 30. Nd2 d5 31. Rae1 a6 32. Ba4 b5 33. Bd1 Rae8 34. Bxg4 Nxg4 35. Re2 Bd3 36. Rxe7 Rxe7 37. Rd1 Re2 38. Nf3 Be4 39. Ne5+ Kf5 40. Nxg4 Kxg4 41. Bxg7 Rxb2 42. c4 Rg2+ 43. Kf1 bxc4 44. Bf6 Rxa2 45. Bg5 Kxg3 46. Rc1 a5 47. Rd1 Rf2+ 48. Ke1 Rxf4 49. Bxf4+ Kxf4 50. Kf2 a4 51. Ra1 Bc2 52. Ra2 Bb3 53. Ra1 d4 54. Ke2 Kg4 55. Rh1 d3+ 56. Kd2 a3 57. Kc3 a2 58. Kb2 a1=Q+ 59. Kxa1 1-0'

    moves = parse_pgn(pgn8)
    move_delay = 500  # milliseconds between moves
    matrices = []
    # print(moves)
    # s = input()

    while run:
        clock.tick(60)  # Limit the frame rate to 60 frames per second
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for move in moves:
            draw_board(WIN)
            draw_pieces(WIN, board)
            pygame.display.flip()  # Update the display
            # print(board.player)
            # print(move)
            # if move == 'Ne2':
            #     print()
            selected_piece, move_coords = board.get_piece_and_move(move)
            possible_moves = selected_piece.get_legal_moves(board)
            if move_coords in possible_moves:
                board.execute_move(selected_piece.position, move_coords)
                matrices.append(board.make_matrix())

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

        draw_board(WIN)
        draw_pieces(WIN, board)
        pygame.display.flip()  # Update the display
        pygame.time.wait(5000)

        run = False

        for matrix in matrices:
            for row in matrix:
                print(row)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
