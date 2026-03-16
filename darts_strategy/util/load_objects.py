import os
import pickle
from .util.find_filenames import find_player_filename

def load_player(player_name):
    filename = find_player_filename(player_name)
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            player = pickle.load(file)
    else:
        raise Exception(f"Player {player} doesn't exist.")
    return player
