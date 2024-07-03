from game.game_processor import GameProcessor

if __name__ == "__main__":
    # Define hyperparameters
    batch_size = 32
    learning_rate = 0.001
    num_epochs = 5
    max_moves_per_game = 20

    NUMBER_OF_GAMES = 100000
    MIN_SCORE = 600 # koliko igara mora da bude odigrano sa tim openingom da bi ga racunali

    # Initialize dataset and model
    processor = GameProcessor()
    with open('C:/Users/milic/Desktop/RI/biii/lichess_db_standard_rated_2016-01.pgn', 'r') as file:
        for i in range(NUMBER_OF_GAMES):  # Adjust the number of games to read as needed
            processor.read_until_string('Event', file)
    processor.filter_games()
    processor.separate_game_into_positions()
    
    print(len(processor.games))
    opening_counter = {}
    balanced_games = []
    for game in processor.games:
        if game['opening'] not in opening_counter.keys():
            opening_counter[game['opening']] = 1
            balanced_games.append(game)
        elif opening_counter[game['opening']] >= MIN_SCORE:
            continue
        else:
            opening_counter[game['opening']] += 1
            balanced_games.append(game)

    # Sort the dictionary by value in descending order
    sorted_dict_desc = dict(sorted(opening_counter.items(), key=lambda item: item[1], reverse=True))
    #print(sorted_dict_desc)
    together = 0
    top100 = []
    for opening_name, score in sorted_dict_desc.items():
        if score >= MIN_SCORE:
            # print(opening_name, "=====", score)
            together += score
            top100.append(opening_name)

    balanced_games = [game for game in balanced_games if game['opening'] in top100]

    # for x,rez in sorted_dict_desc.items():
    #     print(x, "=======",rez)

    print(len(balanced_games))
    print(len(top100))

    # # Split the dataset into training and validation sets
    train_games = []
    val_games = []
    train_games_openings = {opening_name: 0 for opening_name in top100}

    for game in balanced_games:
        if train_games_openings[game['opening']] >= 0.7 * MIN_SCORE:
            val_games.append(game)
        else:
            train_games.append(game)
            train_games_openings[game['opening']] += 1

    # # train_games = balanced_games[:round(len(balanced_games) * 0.7)]
    # # val_games = balanced_games[round(len(balanced_games) * 0.7):]

    print(f"Number of training games: {len(train_games)}")
    print(f"Number of validation games: {len(val_games)}")

    with open("hi.txt", "w") as file:
        for opening in top100:
            file.write(opening + '\n')