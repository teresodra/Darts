import numpy as np
from .objects.cells import Region

def gaussian(x, y, mu, inv_sigma):
    dx = x - mu[0]
    dy = y - mu[1]
    exponent = -0.5 * (dx * (inv_sigma[0][0]*dx + inv_sigma[0][1]*dy) +
                    dy * (inv_sigma[1][0]*dx + inv_sigma[1][1]*dy))
    return np.exp(exponent)

def integrate_gaussian_in_sector_region(aiming_point:tuple,
                                        player,
                                        region:Region,
                                        rgridsize=100,
                                        phigridsize=100):
    if region.max_r == 300 and aiming_point == (220, 0):
        pass
    dr = (region.max_r - region.min_r) / rgridsize
    dphi = (region.max_phi - region.min_phi) / phigridsize
    
    r_values = np.arange(region.min_r, region.max_r, dr)
    phi_values = np.arange(region.min_phi, region.max_phi, dphi)

    r, phi = np.meshgrid(r_values, phi_values, indexing='ij')
    x = r * np.cos(phi)
    y = r * np.sin(phi)

    mu = tuple(a + b for a, b in zip(aiming_point, player.mean))
    
    # Compute gaussian values for all x and y
    gauss_values = gaussian(x, y, mu, player.inv_sigma)
    
    # Compute the integral using the trapezoid rule
    integral = np.sum(gauss_values * r * dr * dphi) / (2 * np.pi * np.sqrt(player.det_sigma))
    
    return integral