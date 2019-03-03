from game.grid.stategrid import StateGrid

class ArrayGrid(StateGrid):
    def __init__(self, rows, columns):
        super(ArrayGrid, self).__init__(rows, columns)

    def initial_state(self):
        return [[0 for _ in range(self.columns)] for _ in range(self.rows)]

    def update(self):
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
