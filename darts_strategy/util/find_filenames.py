import os


def find_player_filename(player_name):
    return os.path.join('players', f'{player_name}.pkl')
