with open("C:/Users/milic/Desktop/RI/biii/lichess_db_standard_rated_2016-01.pgn", "r") as f:
    print(f.read())

# def parse_pgn(pgn_text):
#     games = []
#     current_game = []
#     lines = pgn_text.splitlines()
    
#     for line in lines:
#         if line.startswith('['):
#             # Ignore metadata lines
#             continue
#         if line.strip() == '':
#             # Empty line indicates a new game
#             if current_game:
#                 games.append(' '.join(current_game).strip())
#                 current_game = []
#         else:
#             # Add move to current game
#             current_game.append(line.strip())
    
#     # Add the last game if any
#     if current_game:
#         games.append(' '.join(current_game).strip())
    
#     return games

# # Example usage:
# pgn_text = """
# 1. e4 e5 2. Nf3 d6 3. Bc4 h6 4. d4 Nd7 5. O-O Ngf6 6. dxe5 dxe5 7. Bxf7+ Kxf7 8. Nxe5+ Kg8 9. c3 Qe7 10. Ng6 Qxe4 11. Nxh8 Ne5 12. Qb3+ Kxh8 13. Be3 Be6 14. Qd1 Bd6 15. Nd2 Qg6 16. Nf3 Rf8 17. Nxe5 Bxe5 18. h3 Bxh3 19. g3 Bxf1 20. Kxf1 Ng4 21. Bxa7 b6 22. f4 Ne3+ 0-1

# [Event "Rated Bullet game"]
# [Site "https://lichess.org/FkU1JAS3"]
# [White "rahul680"]
# [Black "bubulubu"]
# [Result "1-0"]
# [UTCDate "2015.12.31"]
# [UTCTime "23:05:40"]
# [WhiteElo "1968"]
# [BlackElo "1921"]
# [WhiteRatingDiff "+9"]
# [BlackRatingDiff "-9"]
# [ECO "A10"]
# [Opening "English Opening: Anglo-Scandinavian Defense"]
# [TimeControl "60+0"]
# [Termination "Normal"]

# 1. c4 d5 2. cxd5 c6 3. dxc6 e6 4. cxb7 Bxb7 5. Nf3 Nf6 6. d4 Bxf3 7. exf3 Nbd7 8. Nc3 Be7 9. d5 exd5 10. Nxd5 Nxd5 11. Qxd5 O-O 12. Bd3 Bf6 13. Qf5 Ne5 14. Qxh7# 1-0

# [Event "Rated Bullet game"]
# [Site "https://lichess.org/im9PmrDs"]
# [White "denis1982777"]
# [Black "Ptitsa02"]
# [Result "1-0"]
# [UTCDate "2015.12.31"]
# [UTCTime "23:05:39"]
# [WhiteElo "1299"]
# [BlackElo "1386"]
# [WhiteRatingDiff "+17"]
# [BlackRatingDiff "-17"]
# [ECO "B30"]
# [Opening "Sicilian Defense: Old Sicilian"]
# [TimeControl "60+0"]
# [Termination "Time forfeit"]

# """

# games = parse_pgn(pgn_text)
# for i, game in enumerate(games):
#     print(f"Game {i+1}:\n{game}\n")

