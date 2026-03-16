import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from .constants import radiuses

def plot_heatmap_from_cartesian_data(data, radiuses=radiuses):
    """
    Generates a heatmap based on Cartesian coordinates and associated probabilities, 
    with optional circular lines at specific radii and rays at specific angles.

    Parameters:
    data (dict): A dictionary where keys are tuples of Cartesian coordinates (x, y) and values are probabilities.
    radiuses (list): A list of radii at which to draw circular lines.

    Returns:
    None
    """
    # Extracting data from the dictionary
    cartesian_coords = list(data.keys())
    probabilities = list(data.values())

    # Split Cartesian coordinates into x and y lists
    x = [coord[0] for coord in cartesian_coords]
    y = [coord[1] for coord in cartesian_coords]

    # Create grid for interpolation
    grid_x, grid_y = np.mgrid[min(x):max(x):200j, min(y):max(y):200j]

    # Interpolate the probabilities over the grid
    grid_z = griddata((x, y), probabilities, (grid_x, grid_y), method='cubic')

    # Plot the heatmap
    plt.figure(figsize=(15, 15))
    plt.imshow(grid_z.T, extent=(min(x), max(x), min(y), max(y)), origin='lower', cmap='viridis')
    cbar = plt.colorbar()
    cbar.set_label('Probability of winning', fontsize=30)
    cbar.ax.tick_params(labelsize=24)
    # Make ticks into percentage 0.05 -> 5%
    cbar.ax.set_yticklabels(['{:.1f}%'.format(i*100) for i in cbar.get_ticks()], fontsize=24)

    # Add circular lines at specified radii
    if radiuses:
        ax = plt.gca()  # Get current axis
        for radius in radiuses[:-1]:  # Skip the last radius as it's not part of the dartboard
            circle = plt.Circle((0, 0), radius, color='black', fill=False, linestyle='-', linewidth=1.5)
            ax.add_artist(circle)

    # Draw rays from the second internal circle to the last one
    inner_radius = radiuses[1]  # The second internal circle (radius 16)
    outer_radius = radiuses[-2]  # The last circle (radius 170)

    # Loop for n < 20 and create rays at angles of pi/20 + pi/10*n
    for n in range(20):
        angle = np.pi / 20 + (n * np.pi / 10)
        x_start = inner_radius * np.cos(angle)
        y_start = inner_radius * np.sin(angle)
        x_end = outer_radius * np.cos(angle)
        y_end = outer_radius * np.sin(angle)

        plt.plot([x_start, x_end], [y_start, y_end], color='black', linestyle='--', linewidth=1.5)

    # Adjust axis limits to ensure all circles and rays are visible
    max_radius = max(radiuses) if radiuses else max(max(x), max(y))
    plt.xlim(-max_radius/2, max_radius/2)
    plt.ylim(-max_radius/2, max_radius/2)

    plt.title('Heatmap of Probabilities of winning depending on aiming point', fontsize=25)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.show()
