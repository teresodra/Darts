import numpy as np
from scipy.integrate import dblquad
from players import Player
from strategies import GameStrategy
from constants import positions

def run_this_fast():
    '''
    This function makes the code user-friendly
    '''


    # starting_points = int(input("With how many points do you start playing?"))
    # n_turns= int(input("In how many turns do you want to end?"))
    # skill = int(input("What is your skill level?(1-50)\n 1->Master of darts \n 50->Sometimes I hit the dartboard \n For reference, someone with skill 20 hits the desired double cell one out of 8 times."))

    starting_points = 101
    n_turns = 10
    skill = 20

    # distance = lambda r, phi, r_P, phi_P: np.sqrt(r_P**2 + r**2 - 2 * r_P * r * np.cos(phi_P - phi))
    # D = lambda r, phi, r_P, phi_P: r * np.exp(-1/2 * (distance(r, phi, r_P, phi_P)/skill)**2)

    print(f"Wait for {starting_points * n_turns * 3 * 6 / 60} minutes")  # in seconds: number of points to calculate, number of turns, 3 darts, 6 seconds for each

    player = Player(((skill^2, 0),(0,skill^2)))
    game_strategy = GameStrategy(player, n_turns=n_turns, max_points=starting_points)
    best_strategy_stored = game_strategy.strategy

    playing = 1
    while playing == 1:
        won = 0
        points = starting_points
        turn = n_turns
        darts_left = 3
        while won == 0 and turn != 0:
            print(f"You have {points} points left.")
            print(f"You have {darts_left} darts left and {turn} turns left.")

            print(best_strategy_stored.keys())

            best_strategy_stored[(turn, darts_left)]
            best_strategy_stored[(turn, darts_left)][points]
            print(best_strategy_stored[(turn, darts_left)][points]['coordinates'])
            best_strategy_stored[(turn, darts_left)][points]['coordinates'][0]

            print('\nposition', best_strategy_stored[(turn, darts_left)][points]['coordinates'][1])

            # position = round(best_strategy_stored[(turn, darts_left)][points]['coordinates'][1] * 20 / (2 * np.pi))
            # r = best_strategy_stored[(turn, darts_left)][points]['coordinates'][0]

            # print('\nposition', position)

            # if r == 0:
            #     print("Aim the bullseye!")
            # else:
            #     print(f"You have to aim to the point of the dartboard with radius {r}", end='')
            #     if type(position) == int:
            #         print('\n', positions, '\n')
            #         print(f" in {positions[position]}")
            #     else:
            #         print('\nint(position+0.5)-1', int(position+0.5)-1)
            #         print(f" between {positions[int(position-0.5)-1]} and {positions[int(position+0.5)-1]}")

            print(f"If you do that, you will end with probability {best_strategy_stored[(turn, darts_left)][points]['probability']}")

            darts_left = darts_left - 1
            points_scored = int(input("How many points did you score?"))

            if points - points_scored > 1:
                points = points - points_scored
            else:
                if points == points_scored:
                    double = int(input("Did you hit a double? (1-Yes/0-No)"))
                    if double == 1:
                        won = 1

                if won == 0:
                    print("You scored too many points, you end this turn")
                    turn = turn - 1
                    darts_left = 3

            if darts_left == 0:
                turn = turn - 1
                darts_left = 3

        if won == 1:
            print("Congratulations! You won!!")
        else:
            print("You lose :'(")

        playing = int(input("Do you want to play again? (1->Yes; 0->No)"))


run_this_fast()