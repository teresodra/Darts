class Game():
    """General description of games."""
    def __init__(self, players, initial_state):
        self.initial_state = initial_state
        self.players = players
        self.players_state = {player:self.initial_state for player in players}
        self.state_probability = dict()


class FirstToZero(Game):
    """This game is won by the first player to reach exactly 0 points."""

    def __init__(self, players, initial_state=101, double_out=True):
        self.double_out = double_out
        super().__init__(players, initial_state)

    def prob_finish_given_probs(self, players_state, probabilities, prev_dart_prob, prev_turn_prob):
        '''
        Calculate the probability of finishing in one dart more than prev_dart_prob if we aim for the point P
        on the dartboard when we have 'points_left' points to go and darts_left darts left.
        '''
        values = list(range(1, 21)) + list(range(2, 41, 2)) + list(range(3, 61, 3)) + [0, 25, 50]
        prob = 0

        for i in range(len(values)):
            if points_left - values[i] > 1:
                # print(points_left)
                prob += prev_dart_prob[points_left - values[i]] * values_prob[i]
            elif values[i] == points_left and ((i >= 20 and i < 40) or i == 62):
                prob += values_prob[i]
            else:
                prob += turn_initial_prob[points_left] * values_prob[i]

        return prob
        