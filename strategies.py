import numpy as np
from given_strategy import give_strategy

class GameStrategy:
    def __init__(self, player, n_turns, max_points, mode='optimal'):
        self.n_turns = n_turns
        self.max_points = max_points
        self.player = player
        self.stored_probabilities = player.grid_probabilities
        self.strategy = self.generating_strategy(mode=mode)

    def prob_finish_given_probs(self, points_left, values_prob, prev_dart_prob, turn_initial_prob):
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

    def grid_search_global_maximum(self, points_left, prev_dart_prob, prev_turn_prob):
        '''
        Perform a grid search on the dartboard to find an approximation of the global maximum.
        '''
        optimal_coordinate = None
        optimal_prob = 0

        for coordinate, probabilities in self.stored_probabilities.items():
            prob_n = self.prob_finish_given_probs(points_left, probabilities, prev_dart_prob, prev_turn_prob)
            if prob_n > optimal_prob:
                optimal_prob = prob_n
                optimal_coordinate = coordinate

        return optimal_coordinate, optimal_prob

    def one_dart_more_strategy_calculator(self, prev_dart_prob, prev_turn_prob):
        '''
        Calculate the strategy to maximize the probability of finishing
        with one dart more than prev_dart_prob.

        Returns best_strategy and probabilities.
        best_strategy is a dictionary with points left as keys.
        Each of this keys store another dictionary with keys 'coordinates' and 'probability'
        containing the optimal coordinate to aim to and the probability of finishing if so.
        '''
        best_strategy = dict()
        probabilities = np.zeros(self.max_points + 1)

        for points_left in range(1, self.max_points + 1):
            optimal_coordinate, optimal_prob = self.grid_search_global_maximum(points_left, prev_dart_prob, prev_turn_prob)
            best_strategy[points_left] = dict()
            best_strategy[points_left]['coordinates'] = optimal_coordinate
            best_strategy[points_left]['probability'] = optimal_prob
            probabilities[points_left] = optimal_prob

        return best_strategy, probabilities

    def generating_strategy(self, mode='optimal'):
        '''
        This function generates the strategy to maximize the probability of finishing in the next n turns
        when throwing according to the distribution D
        '''

        strategy_stored = dict()
        # keys are points left
        # values are dictionaries having 'coordinates' and 'probability' as keys
        prev_dart_prob = np.zeros(self.max_points+1)
        prev_turn_prob = np.zeros(self.max_points+1)
        print(mode)

        if mode == 'given':
            given_strategy = give_strategy(self.max_points)

        for turn in range(self.n_turns + 1):
            for darts_left in range(1, 3 + 1):
                # print('darts', darts_left)
                if mode == 'optimal':
                    strategy, new_prob = self.one_dart_more_strategy_calculator(prev_dart_prob, prev_turn_prob)
                elif mode == 'given':
                    strategy, new_prob = self.add_probabilities(given_strategy, prev_dart_prob, prev_turn_prob)
                else:
                    raise Exception(f"I don't know any strategy called {mode}")
                strategy_stored[(turn, darts_left)] = strategy
                prev_dart_prob = new_prob
            prev_turn_prob = new_prob
        return strategy_stored

    def add_probabilities(self, strategy, prev_dart_prob, prev_turn_prob):
        deduced_strategy = dict()
        probabilities = dict()
        for points_left, coordinates in strategy.items():
            deduced_strategy[points_left] = dict()
            deduced_strategy[points_left]['coordinates'] = coordinates
            probability = self.prob_finish_given_probs(points_left, self.stored_probabilities[coordinates], prev_dart_prob, prev_turn_prob)
            deduced_strategy[points_left]['probability'] = probability
            probabilities[points_left] = probability
        return deduced_strategy, probabilities
