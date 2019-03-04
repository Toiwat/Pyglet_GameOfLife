import numpy as np
from scipy.signal import convolve2d


class _StateGrid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.cells = self.initial_state()
        self.updated = []
        self.generation = 0

    def initial_state(self):
        pass

    def update(self):
        self.generation += 1


    def set_cell_state(self, row: int, col: int, alive: bool):
        self.cells[row, col] = int(alive)
        self.updated.append((row, col))

    def get_updated_cells(self):
        return self.updated


class ArrayGrid(_StateGrid):
    def __init__(self, rows, columns):
        super(ArrayGrid, self).__init__(rows, columns)

    def initial_state(self):
        return [[0 for _ in range(self.columns)] for _ in range(self.rows)]

    def update(self):
        super(ArrayGrid, self).update()

        new_state = self.initial_state()
        self.updated = []

        for i in range(self.rows):
            for j in range(self.columns):
                alive_neighbours = self.alive_neighbours(i, j)
                # Old cell is alive
                if self.is_cell_alive(i, j):
                    if alive_neighbours < 2 or alive_neighbours > 3:
                        # Old cell now dies
                        new_state[i][j] = 0
                        self.updated.append((i, j))
                    else:
                        # Old cell survives
                        new_state[i][j] = 1
                # Old cell was dead
                else:
                    if alive_neighbours == 3:
                        # New cell is born from breeding
                        new_state[i][j] = 1
                        self.updated.append((i, j))

        self.cells = new_state

    def is_cell_alive(self, row, col):
        return self.cells[row][col] == 1

    def alive_neighbours(self, row, col):
        count = 0
        for r in (row-1, row, row+1):
            for c in (col-1, col, col+1):
                if r == row and c == col:  # Don't check the passed cell itself...
                    pass
                else:
                    # Wrap around the opposite edge...
                    if r < 0:
                        r = self.rows-1
                    if c < 0:
                        c = self.columns-1
                    if r >= self.rows:
                        r = 0
                    if c >= self.columns:
                        c = 0

                    if self.cells[r][c] == 1:
                        count += 1

        return count


class NumpyGrid(_StateGrid):
    def __init__(self, rows, columns, rules_kernel=None):
        super(NumpyGrid, self).__init__(rows, columns)

        if rules_kernel is None:
            # Setup default convolution kernel...
            self.rules = np.ones((3, 3))
            self.rules[1][1] = 0
        else:
            self.rules = rules_kernel

    def initial_state(self):
        return np.zeros((self.rows, self.columns))

    def update(self):
        super(NumpyGrid, self).update()

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
