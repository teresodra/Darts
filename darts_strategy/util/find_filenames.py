import os


def find_player_filename(player_name):
    return os.path.join('darts_strategy/players', f'{player_name}.pkl')
