from darts_strategy.players import Player

from .dartboard import DartboardApp

DartboardApp().run()

# game = GameStrategy(player, n_turns=3, max_points=101)
# for i in range(1, 101):
#     j = float(i)
#     my_player = Player(skill=j)
#     probabilities_aiming_centre = my_player.probabilities((0,0))
#     prob_bullseye = probabilities_aiming_centre['bullseye'] + probabilities_aiming_centre['double_bullseye']
#     print(f'Skill: {j}, Probability of hitting the bullseye when aiming for the centre: {prob_bullseye * 100:.1f}% and double {probabilities_aiming_centre["double_bullseye"] * 100:.1f}%')

