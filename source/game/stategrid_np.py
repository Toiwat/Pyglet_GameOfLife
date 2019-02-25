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
        count = convolve2d(self.cells, self.rules, mode='same', boundary='wrap')
        self.cells = np.logical_or((count == 3), np.logical_and((self.cells == 1), (count == 2))).astype(int)

    def set_alive(self, row, col):
        self.cells[row][col] = 1

    def set_dead(self, row, col):
        self.cells[row][col] = 0
