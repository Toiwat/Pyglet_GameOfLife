import numpy as np
from scipy.signal import convolve2d


class StateGridNP:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.cells = np.zeros((rows, columns))
        self.updated = []

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
        new_state = np.logical_or((count == 3), np.logical_and((self.cells == 1), (count == 2)))

        self.updated = [(row, cell) for cell in range(self.columns) for row in range(self.rows)
                        if np.logical_xor(new_state, self.cells.astype(bool))[row, cell]]

        self.cells = new_state.astype(int)

    def set_state(self, row: int, col: int, alive: bool):
        self.cells[row][col] = int(alive)
        self.updated.append((row, col))
