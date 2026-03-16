
import numpy as np
import math

from constants import positions, radiuses

def give_strategy(max_points):
    strategy = dict()
    for points in range(1,max_points+1):
        # triple 20 by default
        radius = (radiuses[2]+radiuses[3])/2
        phi = round(positions.index(20)*np.pi/10, 4)
        strategy[points] = (radius * math.cos(phi),
                                radius * math.sin(phi))

    # we will attempt to land in 50 points with one dart
    for k in range(1,20):
        if 50+3*k<max_points:
            radius = (radiuses[2]+radiuses[3])/2
            phi = round(positions.index(k)*np.pi/10, 4)
            strategy[50+3*k] = (radius * math.cos(phi),
                                radius * math.sin(phi))
    for k in range(1,20):
        if 50+2*k<max_points:
            radius = (radiuses[4]+radiuses[5])/2
            phi = round(positions.index(k)*np.pi/10, 4)
            strategy[50+2*k] = (radius * math.cos(phi),
                                radius * math.sin(phi))
    for k in range(1,20):
        if 50+k<max_points:
            radius = (radiuses[3]+radiuses[4])/2
            phi = round(positions.index(k)*np.pi/10, 4)
            strategy[50+k] = (radius * math.cos(phi),
                                radius * math.sin(phi))
    
    for i in range(1,20):
        # we will attempt to land in a double with one dart
        for k in range(1,20):
            if 2*i+3*k<max_points:
                radius = (radiuses[2]+radiuses[3])/2
                phi = round(positions.index(k)*np.pi/10, 4)
                strategy[2*i+3*k] = (radius * math.cos(phi),
                                    radius * math.sin(phi))
        for k in range(1,20):
            if 2*i+2*k<max_points:
                radius = (radiuses[4]+radiuses[5])/2
                phi = round(positions.index(k)*np.pi/10, 4)
                strategy[2*i+2*k] = (radius * math.cos(phi),
                                    radius * math.sin(phi))
        for k in range(1,20):
            if 2*i+k<max_points:
                radius = (radiuses[3]+radiuses[4])/2
                phi = round(positions.index(k)*np.pi/10, 4)
                strategy[2*i+k] = (radius * math.cos(phi),
                                    radius * math.sin(phi))
    ###
    # If a triple, a double or a single take you to an even between 2 and 40 or 50 go for it.
    # Giving preference to those finishing in a power of 2, and to the higher, exceptuating 50 that has the lowest preference
    ###

    ###
    # If a default strategy is given, follow it
    ###

    for k in range(1,21):
        if 2*k <= max_points:
            radius = (radiuses[4]+radiuses[5])/2
            phi = round(positions.index(k)*np.pi/10, 4)
            strategy[2*k] = (radius * math.cos(phi),
                                radius * math.sin(phi))
    #         # if a double finishes go for it overwriting previous
    # print(list(strategy.keys()))
    return strategy
