
# NORMAL DARTBOARD

radiuses = [6.35, 16, 99, 107, 162, 170, 220]
# radius of the different circles in the dartboard
positions = [6, 13, 4, 18, 1, 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10]
# position of numbers in the dartboard


values = list(range(1, 21)) + list(range(2, 41, 2)) + list(range(3, 61, 3)) + [0, 25, 50]
# values in the dartboard

    


# will include a dictionary of the different possible values, where one 
cells = []
# algo asi para las celdas
        # for i in range(20):
        #     ipos = positions.index(i + 1)
        #     phimin = (ipos - 0.5) * np.pi / 10
        #     phimax = (ipos + 0.5) * np.pi / 10

        #     p[i] = (self.integrate_gaussian(mu, (radiuses[1], radiuses[2]), (phimin, phimax)) +
        #             self.integrate_gaussian(mu, (radiuses[3], radiuses[4]), (phimin, phimax)))    # single
        #     p[20 + i] = self.integrate_gaussian(mu, (radiuses[4], radiuses[5]), (phimin, phimax)) # double
        #     p[40 + i] = self.integrate_gaussian(mu, (radiuses[2], radiuses[3]), (phimin, phimax)) # triple

        # p[60] = self.integrate_gaussian(mu, (radiuses[5], radiuses[6]), (0, 2 * np.pi)) # out
        # p[61] = self.integrate_gaussian(mu, (radiuses[0], radiuses[1]), (0, 2 * np.pi)) # bullseye
        # p[62] = self.integrate_gaussian(mu, (0, radiuses[0]), (0, 2 * np.pi))           # double bullseye