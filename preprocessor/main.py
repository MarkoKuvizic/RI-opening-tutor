from pprint import pprint
games = []
def read_until_string(target_string, file):
    game = {}
    try:
        for line in file:
            #print(line, end='')
            
            if target_string in line:
                break
            elif "Termination" in line:
                game["termination"] = line.split("\"")[1]
            elif "1." in line:
                game["pgn"] = line.strip()
                game["result"] = game["pgn"].split(" ")[-1]
            elif "WhiteElo" in line:
                game["whiteElo"] = eval(line.split("\"")[1])
            elif "BlackElo" in line:
                game["blackElo"] = eval(line.split("\"")[1])
        games.append(game)
    except Exception as e:
        print(f"An error occurred: {e}")
def filter_games():
    global games
    games.pop(0)
    games = [game for game in games if filter_game(game)]
def filter_game(game):
    return game["termination"].lower() != "abandoned" and (game["whiteElo"] + game["blackElo"])/2 > 1500
def separate_game_into_positions(games):
    for game in games:
        pgn = game["pgn"]
        moves = [v.split(" ")[0:2] for v in pgn.split(". ")]
        moves.remove(['1'])
        game["moves"] = moves
with open('lichess_db_standard_rated_2016-01.pgn', 'r') as file:
    for i in range(10):
        read_until_string('Event', file)
filter_games()
separate_game_into_positions(games)
pprint(games)