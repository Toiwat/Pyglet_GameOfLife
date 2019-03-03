class StateGrid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.cells = self.initial_state()
        self.updated = []

    def initial_state(self):
        pass

    def update(self):
        pass

    def set_cell_state(self, row: int, col: int, alive: bool):
        self.cells[row][col] = int(alive)
        self.updated.append((row, col))

    def get_updated_cells(self):
        return self.updated

