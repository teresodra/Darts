import os
import pickle
from util.find_filenames import find_strategy
from players import Player
from strategies import GameStrategy

def next_move(player_name, max_points, points_left, points_scored, last_turn_points, turn, darts_left, mode, hit_double=0):
    # send dictionary instead
    points_left -= points_scored
    win = False
    if points_left == 0:
        if hit_double:
            win = True
            return win, points_left, turn, darts_left, (0,0), 1
        else:
            turn -= 1
            darts_left = 3
            points_left = last_turn_points
    elif points_left <= 1:
        turn -= 1
        darts_left = 3
        points_left = last_turn_points
    else:
        darts_left -= 1
        if darts_left == 0:
            turn -= 1
            darts_left = 3
            last_turn_points = points_left
    strategy = load_strategy(player_name, max_points, mode)
    best_coordinates = strategy[(turn, darts_left)][points_left]['coordinates']
    best_probability = strategy[(turn, darts_left)][points_left]['probability']
    return win, points_left, last_turn_points, turn, darts_left, best_coordinates, best_probability


def load_strategy(player_name, max_points, mode):
    filename = find_strategy(player_name, max_points, mode)
    with open(filename, 'rb') as file:
        strategy = pickle.load(file)
    return strategy


if __name__ == "__main__":
    player_name = 'mario'
    max_points = last_turn_points = points_left = 101
    mode = 'optimal'
    turn = 3
    darts_left = 3
    win = False
    Player(mean=(0,0), sigma=((300,0),(0,300)), name=player_name)
    GameStrategy(player_name, n_turns=turn, max_points=max_points, mode=mode)
    strategy = load_strategy(player_name, max_points, mode)
    best_coordinates = strategy[(turn, darts_left)][points_left]['coordinates']
    best_probability = strategy[(turn, darts_left)][points_left]['probability']
    while not win and (turn>0 or (turn==0 and darts_left==0)):
        print(f"\n\n\n\nTurns: {turn}\nDarts left: {darts_left}")
        print(f"You have {points_left} points left.")
        print(f"If you aim to {best_coordinates} you will finish with probability {best_probability}")
        points_scored = int(input("How many points did you score?"))
        double = False
        if points_scored == points_left:
            double = int(input("Did you hit a double? (1-Yes/0-No)"))
        win, points_left, last_turn_points, turn, darts_left, best_coordinates, best_probability = next_move(player_name, max_points, points_left, points_scored, last_turn_points, turn, darts_left, mode, hit_double=double)
    if win:
        print("You won!")
    else:
        print("You lost :(")