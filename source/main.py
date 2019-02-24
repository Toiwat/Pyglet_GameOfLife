import pyglet
from game.stategrid import StateGrid
from game.spritegrid import SpriteGrid
from math import floor, fabs


class GameOfLife(pyglet.window.Window):
    def __init__(self, window_width, window_height, grid_rows, grid_columns):
        super(GameOfLife, self).__init__(width=window_width, height=window_height,
                                         resizable=False,
                                         caption="Game of Life - Running: False")
        self.win_w = window_width
        self.win_h = window_height

        self.stategrid = StateGrid(grid_rows, grid_columns)
        self.spritegrid = SpriteGrid(self.stategrid, self.win_w, self.win_h)

        self.running = False

    def update(self, dt):
        if self.running:
            self.stategrid = self.stategrid.update()
            self.spritegrid.update(self.stategrid)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.spritegrid.position_in_canvas(x, y):
            cell_row = floor(fabs(self.spritegrid.topleft_y - y) // 16)
            cell_col = floor(fabs(self.spritegrid.topleft_x - x) // 16)

            if button == pyglet.window.mouse.LEFT:
                self.stategrid.cells[cell_row][cell_col] = 1
            elif button == pyglet.window.mouse.RIGHT:
                self.stategrid.cells[cell_row][cell_col] = 0

            self.spritegrid.update(self.stategrid)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self.running = not self.running
            self.set_caption("Game of Life - Running: " + str(self.running))

    def on_draw(self):
        self.clear()
        self.spritegrid.cells_batch.draw()



if __name__ == "__main__":
    window = GameOfLife(1280, 720, 40, 60)

    pyglet.clock.schedule_interval(window.update, 1/10)
    pyglet.app.run()
