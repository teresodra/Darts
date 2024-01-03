import os
import pickle
from find_filenames import find_strategy_filename, find_player_filename
from strategies import GameStrategy


def load_strategy(player_name, max_points, mode, turns:int=5):
    filename = find_strategy_filename(player_name, max_points, mode)
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            strategy = pickle.load(file)
    else:
        strategy = GameStrategy(player_name, n_turns=turns, max_points=max_points, mode=mode).strategy
    return strategy

def load_player(player_name):
    filename = find_player_filename(player_name)
    if os.path.exists(filename):
        with open(filename, 'wb') as file:
            player = pickle.load(file)
    else:
        raise Exception(f"Player {player} doesn't exist.")
    return player
