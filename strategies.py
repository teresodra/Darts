import os
import pickle
import numpy as np
from given_strategy import give_strategy
from players import Player
from util.find_filenames import find_strategy_filename
from util.heatmap import plot_heatmap_from_cartesian_data
from constants import cells

class GameStrategy:
    def __init__(self, player, n_turns, max_points, mode='optimal'):
        # Check the type of 'player'
        if isinstance(player, str):
            # Load the player object from a file if 'player' is a string
            self.player = self.load_player(player)
            self.player_name = player
        elif isinstance(player, Player):
            # Use the player object directly if it's an instance of Player
            self.player = player
            self.player_name = player.name
        else:
            # Raise an error if 'player' is neither a string nor a Player instance
            raise ValueError("The 'player' argument must be either a file path (str) or an instance of the Player class.")

        self.n_turns = n_turns
        self.max_points = max_points
        self.stored_probabilities = self.player.grid_probabilities

        self.strategy = self.generating_strategy(mode=mode)
        filename = find_strategy_filename(self.player.name, max_points, mode)
        with open(filename, 'wb') as file:
            pickle.dump(self.strategy, file)


    def load_player(self, file_name):
        # Construct the full path
        folder = 'players'
        files = [file for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))]
        file_path = os.path.join('players', f'{file_name}.pkl')
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No saved player found at {file_path}")

        with open(file_path, 'rb') as file:
            player = pickle.load(file)
        return player

    def prob_finish_given_probs(self, points_left, values_prob, prev_dart_prob, turn_initial_prob):
        '''
        Calculate the probability of finishing in one dart more than prev_dart_prob if we aim for the point P.
        '''
        prob = 0

        for cell_name, cell in cells.items():
            if points_left - cell.value > 1:
                prob += prev_dart_prob[points_left - cell.value] * values_prob[cell_name]
            elif cell.value == points_left and cell.finish == True:
                prob += values_prob[cell_name]
            else:
                prob += turn_initial_prob[points_left] * values_prob[cell_name]

        return prob

    def grid_search_global_maximum(self, points_left, prev_dart_prob, prev_turn_prob, heatmap=False):
        '''
        Perform a grid search on the dartboard to find an approximation of the global maximum.
        '''
        optimal_coordinate = None
        optimal_prob = 0
        probability_dict = dict()

        for coordinate, probabilities in self.stored_probabilities.items():
            prob_n = self.prob_finish_given_probs(points_left, probabilities, prev_dart_prob, prev_turn_prob)
            if prob_n > optimal_prob:
                optimal_prob = prob_n
                optimal_coordinate = coordinate
            if heatmap:
                # Saving to create a heatmap
                probability_dict[coordinate] = prob_n

        if heatmap:

            plot_heatmap_from_cartesian_data(probability_dict)

        return optimal_coordinate, optimal_prob

    def one_dart_more_strategy_calculator(self, prev_dart_prob, prev_turn_prob, heatmap=False):
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
            if points_left == self.max_points and heatmap:
                my_heatmap = True
            else:
                my_heatmap = False
            optimal_coordinate, optimal_prob = self.grid_search_global_maximum(points_left, prev_dart_prob, prev_turn_prob, heatmap=my_heatmap)
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


        if mode == 'given':
            given_strategy = give_strategy(self.max_points)

        for turn in range(self.n_turns + 1):
            for darts_left in range(1, 3 + 1):
                if turn == self.n_turns and darts_left == 3:
                    heatmap = True
                else:
                    heatmap = False
                if mode == 'optimal':
                    strategy, new_prob = self.one_dart_more_strategy_calculator(prev_dart_prob, prev_turn_prob, heatmap=heatmap)
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
            try:
                prob_of_each_part = self.stored_probabilities[coordinates]
            except KeyError:
                prob_of_each_part = self.player.probabilities(coordinates)
            probability = self.prob_finish_given_probs(points_left, prob_of_each_part, prev_dart_prob, prev_turn_prob)
            deduced_strategy[points_left]['probability'] = probability
            probabilities[points_left] = probability
        return deduced_strategy, probabilities
