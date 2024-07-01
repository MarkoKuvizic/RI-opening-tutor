from pprint import pprint

class GameProcessor():
    def __init__(self):
        self.games = []

    def read_until_string(self, target_string, file):
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
                elif "Opening" in line:
                    game["opening"] = line.split("\"")[1]

            self.games.append(game)
        except Exception as e:
            print(f"An error occurred: {e}")

    def filter_games(self):
        self.games.pop(0)
        self.games = [game for game in self.games if self.filter_game(game)]

    def filter_game(self, game):
        return game["termination"].lower() != "abandoned" and (game["whiteElo"] + game["blackElo"])/2 > 1500
    
    def separate_game_into_positions(self):
        for game in self.games:
            pgn = game["pgn"]
            moves = [v.split(" ")[0:2] for v in pgn.split(". ")]
            moves.remove(['1'])
            game["moves"] = moves

if __name__ == "__main__":
    processor = GameProcessor()
    with open('C:/Users/milic/Desktop/RI/biii/lichess_db_standard_rated_2016-01.pgn', 'r') as file:
        for i in range(10):
            processor.read_until_string('Event', file)
    processor.filter_games()
    processor.separate_game_into_positions()
    pprint(processor.games)