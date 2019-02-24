import pyglet
from game.stategrid import StateGrid
from game.spritegrid import SpriteGrid
from math import floor, fabs


class GameOfLife(pyglet.window.Window):
    def __init__(self, window_width, window_height, grid_rows, grid_columns):
        super(GameOfLife, self).__init__(width=window_width, height=window_height,
                                         resizable=False,
                                         caption="Game of Life")
        self.win_w = window_width
        self.win_h = window_height

        self.stategrid = StateGrid(grid_rows, grid_columns)
        self.spritegrid = SpriteGrid(self.stategrid, self.win_w, self.win_h)

        self.running = False

    def update(self, dt):
        if self.running:
            self.stategrid = self.stategrid.update()
            self.update_sprites()

    def update_sprites(self):
        for i in range(self.stategrid.rows):
            for j in range(self.stategrid.columns):
                if self.stategrid.cells[i][j] == 1:
                    self.spritegrid.sprites[i][j].color = (255, 200, 150)
                elif self.stategrid.cells[i][j] == 0:
                    self.spritegrid.sprites[i][j].color = (255, 255, 255)

    def on_mouse_press(self, x, y, button, modifiers):
        if self.spritegrid.position_in_canvas(x, y):
            cell_row = floor(fabs(self.spritegrid.topleft_y - y) // 16)
            cell_col = floor(fabs(self.spritegrid.topleft_x - x) // 16)

            if button == pyglet.window.mouse.LEFT:
                self.stategrid.cells[cell_row][cell_col] = 1
            elif button == pyglet.window.mouse.RIGHT:
                self.stategrid.cells[cell_row][cell_col] = 0

            self.update_sprites()

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
