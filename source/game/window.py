import pyglet
# from game.grid.numpy_grid import NumpyGrid as StateGrid
from game.grid.array_grid import ArrayGrid as StateGrid
from game.ui.pyglet_opengl import PygletOpenglViewer
from game.ui.pyglet_sprites import PygletSpritesViewer
from math import floor, fabs


class GameOfLife(pyglet.window.Window):
    def __init__(self, window_width=800, window_height=600, grid_rows=15, grid_columns=20, tile_size=32):
        super(GameOfLife, self).__init__(width=window_width, height=window_height,
                                         resizable=False,
                                         caption="Game of Life - Running: False")
        self.width = window_width
        self.height = window_height

        self.stategrid = StateGrid(grid_rows, grid_columns)
        # self.grid = PygletOpenglViewer(self.stategrid, self, tile_size=16, color_dead=(255, 255, 255), color_alive=(100, 100, 100))
        self.grid = PygletSpritesViewer(self.stategrid, self, color_dead=(255, 255, 255), color_alive=(100, 100, 100))

        self.running = False

    def update(self, dt):
        if self.running:
            self.stategrid.update()
            self.grid.update()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.grid.is_position_inside_view_limits(x, y):
            cell_row = floor(fabs(self.grid.top_left.y - y) // self.grid.tile_size)
            cell_col = floor(fabs(self.grid.top_left.x - x) // self.grid.tile_size)

            if button == pyglet.window.mouse.LEFT:
                self.stategrid.set_cell_state(cell_row, cell_col, alive=True)
            elif button == pyglet.window.mouse.RIGHT:
                self.stategrid.set_cell_state(cell_row, cell_col, alive=False)

            self.grid.update()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self.running = not self.running
            self.set_caption("Game of Life - Running: " + str(self.running))

    def on_draw(self):
        self.clear()
        self.grid.batch.draw()
