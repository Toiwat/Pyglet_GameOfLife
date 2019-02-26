import numpy as np
from scipy.signal import convolve2d


class StateGridNP:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.cells = np.zeros((rows, columns))

        # Setup convolution kernel...
        self.rules = np.ones((3, 3))
        self.rules[1][1] = 0

    def update(self):

        # generates a new matrix of same size as self.cells; each element of count is the sum of all living
        # neighbours for the corresponding cell
        count = convolve2d(self.cells, self.rules, mode='same', boundary='wrap')

        # count == 3 returns a boolean matrix for cells with 3 alive neighbours
        # (self.cells == 1 and count == 2) returns a boolean matrix for alive cells with exactly 2 living neighbours
        # logical_and and logical_or are required because Numpy no longer does direct element-wise logical operations
        # for ndarrays
        # astype(int) transforms the resulting boolean matrix into ints for the next state
        self.cells = np.logical_or((count == 3), np.logical_and((self.cells == 1), (count == 2))).astype(int)

    def set_alive(self, row, col):
        self.cells[row][col] = 1

    def set_dead(self, row, col):
        self.cells[row][col] = 0
