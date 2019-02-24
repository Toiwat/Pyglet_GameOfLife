
class StateGrid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.cells = self.zero_state()

    def zero_state(self):
        zero_state = [[0 for col in range(self.columns)] for row in range(self.rows)]
        return zero_state

    def update(self):
        new_grid = StateGrid(self.rows, self.columns)

        for i in range(new_grid.rows):
            for j in range(new_grid.columns):
                alive_neighbours = self.alive_neighbours(i, j)
                # Old cell is alive
                if self.is_cell_alive(i, j):
                    if alive_neighbours < 2 or alive_neighbours > 3:
                        new_grid.cells[i][j] = 0  # Old cell now dies
                    else:
                        new_grid.cells[i][j] = 1  # Old cell survives
                # Old cell was dead
                else:
                    if alive_neighbours == 3:
                        new_grid.cells[i][j] = 1  # New cell is born from breeding

        return new_grid

    def is_cell_alive(self, row, col):
        return (self.cells[row][col] == 1)

    def set_alive(self, row, col):
        self.cells[row][col] = 1

    def set_dead(self, row, col):
        self.cells[row][col] = 0

    def alive_neighbours(self, row, col):
        living_neighbours = 0
        for r in (row-1, row, row+1):
            for c in (col-1, col, col+1):
                if r == row and c == col:  # Don't check the passed cell itself...
                    pass
                elif r < 0 or c < 0 or r >= self.rows or c >= self.columns:  # Don't check out of bounds...
                    pass
                elif self.cells[r][c] == 1:
                    living_neighbours += 1
        return living_neighbours