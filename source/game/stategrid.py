
class StateGrid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.cells = self.zero_state()

    def zero_state(self):
        zero_state = []
        for i in range(self.rows):
            new_row = []
            for j in range(self.columns):
                new_row.append(0)
            zero_state.append(new_row)
        return zero_state

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