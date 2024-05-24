import pygame
IMG_DIR = ".\\game\\img\\"
PIECES = {
    "wp": pygame.image.load(IMG_DIR + "wp.png"),  # White Pawn
    "bp": pygame.image.load(IMG_DIR + "bp.png"),  # Black Pawn
    "wr": pygame.image.load(IMG_DIR + "wr.png"),  # White Rook
    "br": pygame.image.load(IMG_DIR + "br.png"),  # Black Rook
    "wn": pygame.image.load(IMG_DIR + "wn.png"),  # White Knight
    "bn": pygame.image.load(IMG_DIR + "bn.png"),  # Black Knight
    "wb": pygame.image.load(IMG_DIR + "wb.png"),  # White Bishop
    "bb": pygame.image.load(IMG_DIR + "bb.png"),  # Black Bishop
    "wq": pygame.image.load(IMG_DIR + "wq.png"),  # White Queen
    "bq": pygame.image.load(IMG_DIR + "bq.png"),  # Black Queen
    "wk": pygame.image.load(IMG_DIR + "wk.png"),  # White King
    "bk": pygame.image.load(IMG_DIR + "bk.png"),  # Black King
}