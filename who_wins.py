from players import Player
from strategies import GameStrategy

skill1 = 200
skill2 = 300
player1 = Player(((skill1^2, 0), (0, skill1^2)))
player2 = Player(((skill2^2, 0), (0, skill2^2)))

n_turns = 10
points = 301
strategy1 = GameStrategy(player=player1, n_turns=n_turns, max_points=points).generating_strategy()
strategy2 = GameStrategy(player=player2, n_turns=n_turns, max_points=points).generating_strategy()


def prob_first_wins(strategy1, strategy2):
    # winning in the first turn
    player1_wins_prob = strategy1[(0, 3)][points]['probability']
    for n_turn in range(1, n_turns+1):
        # we add the probability of player2 not finishing in the first n_turn turns
        #  but player1 finishing exactly on that turn
        player1_wins_prob += ((1 - strategy2[(n_turn, 3)][points]['probability']) *
                            (strategy1[(n_turn, 3)][points]['probability'] - strategy1[(n_turn-1, 3)][points]['probability'])
                            )
    return player1_wins_prob

print(prob_first_wins(strategy1, strategy2))
print(prob_first_wins(strategy2, strategy1))