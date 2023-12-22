import os
import pickle
import math
import numpy as np
from constants import radiuses, positions

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
            mean, sigma = self.create_distribution(None, points=points)
        self.sigma = sigma
        self.det_sigma = sigma[0][0]*sigma[1][1] - sigma[0][1]*sigma[1][0]
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

    def create_distribution(self, points:list, dartboard:dict, force_mean_0:bool=False):
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

    def gaussian(self, x, y, mu):
        dx = x - mu[0]
        dy = y - mu[1]
        exponent = -0.5 * (dx * (self.inv_sigma[0][0]*dx + self.inv_sigma[0][1]*dy) +
                        dy * (self.inv_sigma[1][0]*dx + self.inv_sigma[1][1]*dy))
        return np.exp(exponent)

    def integrate_gaussian(self, mu, r_bounds, phi_bounds, rgridsize=50, phigridsize=50):
        dr = (r_bounds[1] - r_bounds[0]) / rgridsize
        dphi = (phi_bounds[1] - phi_bounds[0]) / phigridsize
        
        r_values = np.arange(r_bounds[0], r_bounds[1], dr)
        phi_values = np.arange(phi_bounds[0], phi_bounds[1], dphi)

        r, phi = np.meshgrid(r_values, phi_values, indexing='ij')
        x = r * np.cos(phi)
        y = r * np.sin(phi)
        
        # Compute gaussian values for all x and y
        gauss_values = self.gaussian(x, y, mu)
        
        # Compute the integral using the trapezoid rule
        integral = np.sum(gauss_values * r * dr * dphi) / (2 * np.pi * np.sqrt(self.det_sigma))
        
        return integral


    def generate_grid_probabilities(self, phi_grid_size=20, r_grid_size=2):
        if r_grid_size % 2 == 1:
            r_grid_size += 1
            # We want to ensure the grid is even so that the central points of the cells are a posibility
        grid_probabilities = dict()
        grid_probabilities[(0,0)] = self.probabilities((0, 0))

        radiuses_grid = [(k * radiuses[i] + (r_grid_size-k) * radiuses[i+1])/r_grid_size
                         for k in range(r_grid_size+1)
                         for i in range(len(radiuses)-1)]
        # radiuses considered in the grid studied
        for phi in np.arange(0, (2 * math.pi), (2 * math.pi) / phi_grid_size):
            for radius in radiuses_grid:
                aiming_point = (radius * math.cos(phi), radius * math.sin(phi))
                grid_probabilities[(radius, round(phi,4))] = self.probabilities(aiming_point)
        return grid_probabilities

    def probabilities(self, aiming_point):
        '''
        Calculate the probability of hitting every part of the dartboard when aiming for aiming_point
        and following the distribution D. The returned vector contains the probabilities of hitting 1-20
        (first 20 positions), hitting double 1-20 (20-39 positions), hitting triple 1-20 (40-59 positions),
        missing (60), hitting bullseye (61), and double bullseye (62).
        ''' 
        mu = tuple(a + b for a, b in zip(aiming_point, self.mean))
        p = np.zeros(63)
        for i in range(20):
            ipos = positions.index(i + 1)
            phimin = (ipos - 0.5) * np.pi / 10
            phimax = (ipos + 0.5) * np.pi / 10

            p[i] = (self.integrate_gaussian(mu, (radiuses[1], radiuses[2]), (phimin, phimax)) +
                    self.integrate_gaussian(mu, (radiuses[3], radiuses[4]), (phimin, phimax)))
            p[20 + i] = self.integrate_gaussian(mu, (radiuses[4], radiuses[5]), (phimin, phimax))
            p[40 + i] = self.integrate_gaussian(mu, (radiuses[2], radiuses[3]), (phimin, phimax))

        p[60] = self.integrate_gaussian(mu, (radiuses[5], radiuses[6]), (0, 2 * np.pi))
        p[61] = self.integrate_gaussian(mu, (radiuses[0], radiuses[1]), (0, 2 * np.pi))
        p[62] = self.integrate_gaussian(mu, (0, radiuses[0]), (0, 2 * np.pi))

        p = p / np.sum(p)
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


