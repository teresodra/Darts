import math
import numpy as np
from constants import radiuses, positions, radiuses_grid

class Player:
    def __init__(self, sigma=((300, 0), (0, 300))):
        self.sigma = sigma
        self.det_sigma = sigma[0][0]*sigma[1][1] - sigma[0][1]*sigma[1][0]
        self.inv_sigma = (
            (sigma[1][1]/self.det_sigma, -sigma[0][1]/self.det_sigma), 
            (-sigma[1][0]/self.det_sigma, sigma[0][0]/self.det_sigma)
        )
        self.grid_probabilities = self.generate_grid_probabilities()

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


    def generate_grid_probabilities(self, phi_grid_size=20, r_grid_size=3):
        grid_probabilities = dict()
        grid_probabilities[(0,0)] = self.probabilities((0, 0))
        for phi in np.arange(0, (2 * math.pi), (2 * math.pi) / phi_grid_size):
            for radius in radiuses_grid:
                mu = (radius * math.cos(phi), radius * math.sin(phi))
                grid_probabilities[(radius, phi)] = self.probabilities(mu)
        return grid_probabilities

    def probabilities(self, mu):
        '''
        Calculate the probability of hitting every part of the dartboard when aiming for P = [r_P, phi_P]
        and following the distribution D. The returned vector contains the probabilities of hitting 1-20
        (first 20 positions), hitting double 1-20 (20-39 positions), hitting triple 1-20 (40-59 positions),
        missing (60), hitting bullseye (61), and double bullseye (62).
        ''' 
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

# player = Player()
# game = GameStrategy(player, n_turns=3, max_points=101)


