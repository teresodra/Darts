from Objects.cells import Cell, Region
import numpy as np
# NORMAL DARTBOARD

radiuses = [6.35, 16, 99, 107, 162, 170, 220]
# radius of the different circles in the dartboard
positions = [6, 13, 4, 18, 1, 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10]
# position of numbers in the dartboard

    


# will include a dictionary of the different possible values, where one 
cells = dict()
# algo asi para las celdas
for n in range(1, 21):
        npos = positions.index(n)
        phimin = (npos - 0.5) * np.pi / 10
        phimax = (npos + 0.5) * np.pi / 10

        regions_single = [Region(radiuses[1], radiuses[2], phimin, phimax), Region(radiuses[3], radiuses[4], phimin, phimax)]
        regions_double = [Region(radiuses[4], radiuses[5], phimin, phimax)]
        regions_triple = [Region(radiuses[2], radiuses[3], phimin, phimax)]

        cells["single_" + str(n)] = Cell(n, regions_single, False)
        cells["double_" + str(n)] = Cell(n * 2, regions_double, True)
        cells["triple_" + str(n)] = Cell(n * 3, regions_triple, False)
cells["out"] = Cell(0, [Region(radiuses[5], radiuses[6], 0, 2 * np.pi)], False)
cells["bullseye"] = Cell(25, [Region(radiuses[0], radiuses[1], 0, 2 * np.pi)], False)
cells["double_bullseye"] = Cell(50, [Region(0, radiuses[0], 0, 2 * np.pi)], True)