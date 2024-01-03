import os
import pickle


def find_strategy_filename(player_name, max_points, mode):
    return os.path.join('strategies', f'{player_name}-{max_points}-{mode}.txt')


def find_player_filename(player_name):
    return os.path.join('players', f'{player_name}.pkl')
