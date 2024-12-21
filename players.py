import os
import pickle
import math
import numpy as np
from constants import radiuses, positions, cells
from util.integrate import integrate_gaussian_in_sector_region

from scipy.stats import chi2
import numpy.linalg as linalg
from matplotlib import patches
import matplotlib.pyplot as plt

class Player:
    def __init__(self,
                 create_distribution = False,
                 mean = (0,0),
                 sigma=((300, 0), (0, 300)),
                 points = np.array([[10, 20], [20, 10], [30, 40], [40, 30]]),
                 name='player'):
        self.name = name
        if create_distribution:
            mean, sigma = self.create_distribution(points=points)
        self.sigma = sigma
        print(self.sigma, "self.sigma")
        self.det_sigma = sigma[0][0]*sigma[1][1] - sigma[0][1]*sigma[1][0]
        print(self.sigma, "self.sigma")
        print(self.det_sigma, "self.detsingma")
        self.inv_sigma = (
            (sigma[1][1]/self.det_sigma, -sigma[0][1]/self.det_sigma), 
            (-sigma[1][0]/self.det_sigma, sigma[0][0]/self.det_sigma)
        )
        self.mean = mean
        self.grid_probabilities = self.generate_grid_probabilities()
        self.save_to_file()

    def save_to_file(self):
        if not os.path.exists('players'):
            os.makedirs('players')
        with open(f'players/{self.name}.pkl', 'wb') as file:
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
        print(p["out"], "p_out")
        print(p["out_not_considered"], "p_out_not_considered")
        print(sum_p, "sum_p")
        if sum_p < 0.5:
            print(aiming_point, "aiming_point")
            for cell_name in p:
                print(cell_name, p[cell_name])
            f =dfa
        for cell_name in p:
            p[cell_name] = p[cell_name] / sum_p
        
        return p
    
    def visual(self):

        # Eigenvalues and eigenvectors
        eigenvalues, eigenvectors = linalg.eigh(self.sigma)

        # Scaling factor for 50% coverage (chi-square quantile at 50% with 2 degrees of freedom)
        scale_factor = np.sqrt(chi2.ppf(0.5, 2))

        # Lengths of the semi-axes
        axes_lengths = scale_factor * np.sqrt(eigenvalues)

        # Angle of rotation for the ellipse
        angle = np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0])

        # Calculate the extents of the ellipse
        x_radius = axes_lengths[0]
        y_radius = axes_lengths[1]
        left_extent = self.mean[0] - x_radius
        right_extent = self.mean[0] + x_radius
        bottom_extent = self.mean[1] - y_radius
        top_extent = self.mean[1] + y_radius

        # Add some padding
        padding = max(x_radius, y_radius) * 0.1  # 10% padding

        # Plotting
        fig, ax = plt.subplots()
        ellipse = patches.Ellipse(xy=self.mean, width=2*axes_lengths[0], height=2*axes_lengths[1], 
                                angle=np.degrees(angle), edgecolor='r', fc='None', lw=2, label='50% Coverage Ellipse')
        ax.add_patch(ellipse)

        # Adjust axes limits
        ax.set_xlim(left_extent - padding, right_extent + padding)
        ax.set_ylim(bottom_extent - padding, top_extent + padding)

        ax.set_aspect('equal', 'datalim')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Ellipse Covering 50% of Points')
        plt.legend()
        plt.show()


if __name__ == '__main__':

    player = Player()
    player.visual()
    # game = GameStrategy(player, n_turns=3, max_points=101)


