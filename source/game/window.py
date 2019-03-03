import pyglet
from game.grid.numpy_grid import NumpyGrid
from game.ui.pyglet_opengl import PygletOpenglViewer
from math import floor, fabs


class GameOfLife(pyglet.window.Window):
    def __init__(self, window_width=800, window_height=600, grid_rows=15, grid_columns=20, tile_size=32):
        super(GameOfLife, self).__init__(width=window_width, height=window_height,
                                         resizable=False,
                                         caption="Game of Life - Running: False")
        self.width = window_width
        self.height = window_height

        self.state_grid = NumpyGrid(grid_rows, grid_columns)
        self.viewer = PygletOpenglViewer(self.state_grid, self, tile_size=tile_size,
                                         color_dead=(255, 255, 255), color_alive=(100, 100, 100))

        self.running = False

    def update(self, dt):
        if self.running:
            self.state_grid.update()
            self.viewer.update()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.viewer.is_position_inside_view_limits(x, y):
            cell_row = floor(fabs(self.viewer.top_left.y - y) // self.viewer.tile_size)
            cell_col = floor(fabs(self.viewer.top_left.x - x) // self.viewer.tile_size)

            if button == pyglet.window.mouse.LEFT:
                self.state_grid.set_cell_state(cell_row, cell_col, alive=True)
            elif button == pyglet.window.mouse.RIGHT:
                self.state_grid.set_cell_state(cell_row, cell_col, alive=False)

            self.viewer.update()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self.running = not self.running
            self.set_caption("Game of Life - Running: " + str(self.running))

    def on_draw(self):
        self.clear()
        self.viewer.batch.draw()
