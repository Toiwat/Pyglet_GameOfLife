import pyglet
from game.stategrid import StateGrid
from game import resources

class SpriteGrid:
    def __init__(self, stategrid: StateGrid, win_w, win_h):
        self.rows = stategrid.rows
        self.columns = stategrid.columns
        self.sprites = []

        self.win_w = win_w
        self.win_h = win_h
        self.grid_h = stategrid.rows * 16
        self.grid_w = stategrid.columns * 16

        self.topleft_x = 0
        self.topleft_y = 0
        self.bottomright_x = 0
        self.bottomright_y = 0

        self.cells_batch = pyglet.graphics.Batch()

        self.setup_canvas_limits()
        self.setup_sprites()

    def setup_canvas_limits(self):
        self.topleft_x = (self.win_w - self.grid_w) // 2
        self.topleft_y = (self.win_h + self.grid_h) // 2
        self.bottomright_x = self.topleft_x + self.grid_w
        self.bottomright_y = self.topleft_y - self.grid_h

    def position_in_canvas(self, x, y):
        return (x > self.topleft_x and y < self.topleft_y) and (x < self.bottomright_x and y > self.bottomright_y)

    def setup_sprites(self):
        for i in range(self.rows):
            new_sprites_row = []
            for j in range(self.columns):
                new_sprites_row.append(
                    pyglet.sprite.Sprite(img=resources.x16_with_border,
                                         x=self.topleft_x+(j*16), y=self.topleft_y-(i*16),
                                         batch=self.cells_batch)
                )
            self.sprites.append(new_sprites_row)