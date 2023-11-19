
import numpy as np

from constants import positions, radiuses

def give_strategy(max_points):
    strategy = dict()
    for points in range(1,max_points+1):
        strategy[points] = (0,0)  # bullseye by default

    # we will attempt to land in 50 points with one dart
    for k in range(1,20):
        if 50+3*k<max_points:
            strategy[50+3*k] = ((radiuses[2]+radiuses[3])/2,
                                round(positions.index(k)*np.pi/10, 4))
    for k in range(1,20):
        if 50+2*k<max_points:
            strategy[50+2*k] = ((radiuses[4]+radiuses[5])/2,
                                round(positions.index(k)*np.pi/10, 4))
    for k in range(1,20):
        if 50+k<max_points:
            strategy[50+k] = ((radiuses[3]+radiuses[4])/2,
                                round(positions.index(k)*np.pi/10, 4))
    
    for i in range(1,20):
        # we will attempt to land in a double with one dart
        for k in range(1,20):
            if 2*i+3*k<max_points:
                strategy[2*i+3*k] = ((radiuses[2]+radiuses[3])/2,
                                    round(positions.index(k)*np.pi/10, 4))
        for k in range(1,20):
            if 2*i+2*k<max_points:
                strategy[2*i+2*k] = ((radiuses[4]+radiuses[5])/2,
                                    round(positions.index(k)*np.pi/10, 4))
        for k in range(1,20):
            if 2*i+k<max_points:
                strategy[2*i+k] = ((radiuses[3]+radiuses[4])/2,
                                    round(positions.index(k)*np.pi/10, 4))
    ###
    # If a triple, a double or a single take you to an even between 2 and 40 or 50 go for it.
    # Giving preference to those finishing in a power of 2, and to the higher, exceptuating 50 that has the lowest preference
    ###

    ###
    # If a default strategy is given, follow it
    ###

    for k in range(1,21):
        if 2*k <= max_points:
            strategy[2*k] = ((radiuses[4]+radiuses[5])/2,
                             round(positions.index(k)*np.pi/10, 4))
    #         # if a double finishes go for it overwriting previous
    # print(list(strategy.keys()))
    return strategy
