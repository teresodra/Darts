import os
import pickle
import math
import numpy as np
from constants import radiuses, cells
from util.integrate import integrate_gaussian_in_sector_region

class Player:
    def __init__(self,
                 skill=20,
                 mean = (0,0),
                 name='player'):
        
        self.name = name
        self.mean = mean
        self.skill = skill
        self.sigma = ((skill**2, 0), (0, skill**2))

        self.det_sigma = self.sigma[0][0]*self.sigma[1][1] - self.sigma[0][1]*self.sigma[1][0]
        self.inv_sigma = (
            (self.sigma[1][1]/self.det_sigma, -self.sigma[0][1]/self.det_sigma), 
            (-self.sigma[1][0]/self.det_sigma, self.sigma[0][0]/self.det_sigma)
        )

        # Check if the grid probabilities file already exists
        if os.path.exists(f'players/skill_{skill}.pkl'):
            with open(f'players/skill_{skill}.pkl', 'rb') as file:
                saved_player = pickle.load(file)
                self.grid_probabilities = saved_player.grid_probabilities
        else:
            self.grid_probabilities = self.generate_grid_probabilities()
            self.save_to_file()

    def save_to_file(self):
        if not os.path.exists('players'):
            os.makedirs('players')
        with open(f'players/skill_{self.skill}.pkl', 'wb') as file:
            pickle.dump(self, file)

    def create_distribution(self, points:list, dartboard:dict=None, force_mean_0:bool=False):
        """
        This function will compute the throwing distribution of the player.
        points is a list of 2-tuples giving the coordinates of the points the user clicked
        dartboard is a dictionary with two keys
            - 'centre' whose value is a 2-tuple giving the coordinates of the centre in the screen
            - 'diametre' whose value is the diametre of the dartboard in the screen
        """

        # Transform points to real distances

        # Calculate the mean and sigma of the data
        if force_mean_0:
            mean = 0
            sigma = np.dot(points.T, points) / len(points)
        else:
            mean = np.mean(points, axis=0)
            sigma = np.cov(points, rowvar=False)

        return mean, sigma


    def generate_grid_probabilities(self, phi_grid_size=20, r_grid_size=5):
        if r_grid_size % 2 == 0:
            r_grid_size += 1
            # We want to ensure the grid is odd so that the central points of the cells are a posibility
        grid_probabilities = dict()
        grid_probabilities[(0,0)] = self.probabilities((0, 0))

        radiuses_grid = [(k * radiuses[i] + (r_grid_size-k) * radiuses[i+1])/r_grid_size
                         for k in range(r_grid_size)
                         for i in range(len(radiuses)-2)] # we dont consider points in the outermost circle
        # radiuses considered in the grid studied
        phi_grid = np.arange(0, (2 * math.pi), (2 * math.pi) / phi_grid_size)

        for phi in phi_grid:
            for radius in radiuses_grid:
                aiming_point = (radius * math.cos(phi), radius * math.sin(phi))
                grid_probabilities[aiming_point] = self.probabilities(aiming_point)
                print(aiming_point, grid_probabilities[aiming_point])
        return grid_probabilities

    def probabilities(self, aiming_point):
        '''
        Calculate the probability of hitting every part of the dartboard when aiming for aiming_point
        and following the distribution D. The returned dictionary contains the probabilities of hitting each cell.
        ''' 
        p = dict()
        for cell_name, cell in cells.items():
            p[cell_name] = 0
            for region in cell.regions:
                p[cell_name] += integrate_gaussian_in_sector_region(aiming_point=aiming_point,
                                                                    player=self,
                                                                    region=region)
        # sum all values of p and standarise them to add to 1        
        sum_p = sum(p.values())
        for cell_name in p:
            p[cell_name] = p[cell_name] / sum_p
        
        return p


if __name__ == '__main__':

    # game = GameStrategy(player, n_turns=3, max_points=101)
    for i in range(1, 101):
        j = float(i)
        my_player = Player(skill=j)
        probabilities_aiming_centre = my_player.probabilities((0,0))
        prob_bullseye = probabilities_aiming_centre['bullseye'] + probabilities_aiming_centre['double_bullseye']
        print(f'Skill: {j}, Probability of hitting the bullseye when aiming for the centre: {prob_bullseye}')

