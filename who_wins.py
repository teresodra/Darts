from players import Player
from strategies import GameStrategy

skill1 = 300
skill2 = 200
player1 = Player(sigma=((skill1^2, 0), (0, skill1^2)))
player2 = Player(sigma=((skill2^2, 0), (0, skill2^2)))

n_turns = 20
points = 301
strat_given = GameStrategy(player=player1, n_turns=n_turns, max_points=points, mode='given').strategy

strat_optimal = GameStrategy(player=player2, n_turns=n_turns, max_points=points, mode='given').strategy


def prob_first_wins(strategy1, strategy2):
    # winning in the first turn
    player1_wins_prob = strategy1[(0, 3)][points]['probability']
    player2_wins_prob = 0
    for n_turn in range(1, n_turns+1):
        # we add the probability of player2 not finishing in the first n_turn turns
        #  but player1 finishing exactly on that turn
        player1_wins_prob += ((1 - strategy2[(n_turn-1, 3)][points]['probability']) *
                            (strategy1[(n_turn, 3)][points]['probability'] - strategy1[(n_turn-1, 3)][points]['probability'])
                            )
        player2_wins_prob += ((1 - strategy1[(n_turn, 3)][points]['probability']) *
                            (strategy2[(n_turn, 3)][points]['probability'] - strategy2[(n_turn-1, 3)][points]['probability'])
                            )
    print(player1_wins_prob+player2_wins_prob)
    return player1_wins_prob

print(prob_first_wins(strat_given, strat_optimal))
print(prob_first_wins(strat_optimal, strat_given))