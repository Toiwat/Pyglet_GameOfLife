import pyglet
from game.grid.numpy_grid import NumpyGrid as StateGrid


class oglGrid:
    def __init__(self, stategrid: StateGrid, win_w, win_h, tile_size=16):
        self.rows = stategrid.rows
        self.columns = stategrid.columns

        self.tile_size = tile_size

        self.win_w = win_w
        self.win_h = win_h
        self.grid_h = stategrid.rows * self.tile_size
        self.grid_w = stategrid.columns * self.tile_size

        self.topleft_x = 0
        self.topleft_y = 0
        self.bottomright_x = 0
        self.bottomright_y = 0

        self.batch = pyglet.graphics.Batch()
        self.vertex_list = []
        self.color_list = []

        self.setup_canvas_limits()
        self.setup()

    def setup_canvas_limits(self):
        self.topleft_x = (self.win_w - self.grid_w) // 2
        self.topleft_y = (self.win_h + self.grid_h) // 2
        self.bottomright_x = self.topleft_x + self.grid_w
        self.bottomright_y = self.topleft_y - self.grid_h

    def position_in_canvas(self, x, y):
        return (x > self.topleft_x and y < self.topleft_y) and (x < self.bottomright_x and y > self.bottomright_y)

    def setup(self):
        vertex_data = []
        for i in range(self.rows):
            for j in range(self.columns):
                vertex_data.append(
                    [self.topleft_x+(j*self.tile_size), self.topleft_y-(i*self.tile_size),
                     self.topleft_x+(j*self.tile_size), self.topleft_y-(i*self.tile_size) -self.tile_size+1,
                     self.topleft_x+(j*self.tile_size) +self.tile_size-1, self.topleft_y-(i*self.tile_size) -self.tile_size+1,
                     self.topleft_x+(j*self.tile_size) +self.tile_size-1, self.topleft_y-(i*self.tile_size)]
                )

        vertex_data = [vertex for quad in vertex_data for vertex in quad]

        self.color_list = (255, 255, 255) * self.rows * self.columns * 4
        self.vertex_list = self.batch.add(
            self.rows * self.columns * 4,
            pyglet.gl.GL_QUADS,
            None,
            ('v2i', vertex_data),
            ('c3B', self.color_list)
        )

    def update(self, stategrid):
        for cell in stategrid.updated:
            i = cell[0]
            j = cell[1]
            vert_index = (self.columns * 4 * i) + j * 4
            color_index = vert_index * 3
            if stategrid.cells[i][j] == 1:
                self.vertex_list.colors[color_index:color_index+12] = [50, 50, 50]*4
            else:
                self.vertex_list.colors[color_index:color_index + 12] = [255, 255, 255] * 4
