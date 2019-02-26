import pyglet
# from game.stategrid import StateGrid
from game.stategrid_np import StateGridNP as StateGrid
# from game.spritegrid import SpriteGrid
from game.gl_renderer import oglGrid
from math import floor, fabs


class GameOfLife(pyglet.window.Window):
    def __init__(self, window_width=800, window_height=600, grid_rows=15, grid_columns=20, tile_size=32):
        super(GameOfLife, self).__init__(width=window_width, height=window_height,
                                         resizable=False,
                                         caption="Game of Life - Running: False")
        self.win_w = window_width
        self.win_h = window_height

        self.stategrid = StateGrid(grid_rows, grid_columns)
        # self.grid = SpriteGrid(self.stategrid, self.win_w, self.win_h)
        self.grid = oglGrid(self.stategrid, self.win_w, self.win_h, tile_size)

        self.running = False

    def update(self, dt):
        if self.running:
            self.stategrid.update()
            self.grid.update(self.stategrid)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.grid.position_in_canvas(x, y):
            cell_row = floor(fabs(self.grid.topleft_y - y) // self.grid.tile_size)
            cell_col = floor(fabs(self.grid.topleft_x - x) // self.grid.tile_size)

            if button == pyglet.window.mouse.LEFT:
                self.stategrid.set_alive(cell_row, cell_col)
            elif button == pyglet.window.mouse.RIGHT:
                self.stategrid.set_dead(cell_row, cell_col)

            self.grid.update(self.stategrid)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self.running = not self.running
            self.set_caption("Game of Life - Running: " + str(self.running))

    def on_draw(self):
        self.clear()
        self.grid.batch.draw()
