import os


def find_strategy(player_name, max_points, mode):
    return os.path.join('strategies', f'{player_name}-{max_points}-{mode}.txt')
