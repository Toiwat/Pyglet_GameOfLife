import pyglet
import gameoflife as gol
from collections import namedtuple

Coord = namedtuple("Coord", "x y")


class _Viewer:
    def __init__(self, state_grid: gol.grid._StateGrid, window, tile_size, color_dead, color_alive):

        # Store handles to window and game state grid
        self.window = window
        self.state_grid = state_grid

        # Tile size for the cells
        self.tile_size = tile_size

        # Colors for alive and dead cells
        self.color_dead = color_dead
        self.color_alive = color_alive

        # Size of view area in pixels
        self.view_height = self.state_grid.rows * self.tile_size
        self.view_width = self.state_grid.columns * self.tile_size

        # Coordinates for corners of view area rectangle
        self.top_left = Coord(0, 0)
        self.bottom_right = Coord(0, 0)

        # Pyglet batch object for rendering
        self.batch = pyglet.graphics.Batch()
        self.setup_view_coords()
        self.setup()

    def setup_view_coords(self):
        self.top_left = Coord(
            (self.window.width - self.view_width) // 2,
            (self.window.height + self.view_height) // 2
        )
        self.bottom_right = Coord(
            self.top_left.x + self.view_width,
            self.top_left.y - self.view_height
        )

    def is_position_inside_view_limits(self, x, y):
        return (x > self.top_left.x and y < self.top_left.y) and (x < self.bottom_right.x and y > self.bottom_right.y)

    def setup(self):
        pass

    def update(self):
        pass


class PygletSpritesViewer(_Viewer):
    def __init__(self, state_grid: gol.grid._StateGrid, window, color_dead=(255, 255, 255), color_alive=(50, 50, 50)):
        # List for pyglet sprites
        self.sprites = []
        super(PygletSpritesViewer, self).__init__(state_grid, window, tile_size=16, color_alive=color_alive, color_dead=color_dead)

    def setup(self):
        self.sprites = [[pyglet.sprite.Sprite(img=gol.resources.x16_with_border,
                                x=self.top_left.x+(j*self.tile_size), y=self.top_left.y-(i*self.tile_size),
                                batch=self.batch)
                         for j in range(self.state_grid.columns)] for i in range(self.state_grid.rows)]

    def update(self):
        for i in range(self.state_grid.rows):
            for j in range(self.state_grid.columns):
                if self.state_grid.cells[i][j] == 1:
                    self.sprites[i][j].color = self.color_alive
                elif self.state_grid.cells[i][j] == 0:
                    self.sprites[i][j].color = self.color_dead


class PygletOpenglViewer(_Viewer):
    def __init__(self, state_grid: gol.grid._StateGrid, window, tile_size=16, color_dead=(255, 255, 255), color_alive=(50, 50, 50)):
        # OpenGL vertex and vertex color data
        self.vertex_list = []
        self.color_list = []
        super(PygletOpenglViewer, self).__init__(state_grid, window, tile_size, color_alive, color_dead)

    def setup(self):
        vertex_data = []
        for i in range(self.state_grid.rows):
            for j in range(self.state_grid.columns):
                vertex_data.append(
                    [self.top_left.x+(j*self.tile_size), self.top_left.y-(i*self.tile_size),
                     self.top_left.x+(j*self.tile_size), self.top_left.y-(i*self.tile_size) - self.tile_size+1,
                     self.top_left.x+(j*self.tile_size) + self.tile_size-1, self.top_left.y-(i*self.tile_size) -self.tile_size+1,
                     self.top_left.x+(j*self.tile_size) + self.tile_size-1, self.top_left.y-(i*self.tile_size)]
                )

        vertex_number = self.state_grid.rows * self.state_grid.columns * 4
        vertex_data = [vertex for quad in vertex_data for vertex in quad]

        # Color list needs to exist as a field to be able to change vertex colors
        self.color_list = (255, 255, 255) * vertex_number
        self.vertex_list = self.batch.add(
            vertex_number,
            pyglet.gl.GL_QUADS,
            None,
            ('v2i', vertex_data),
            ('c3B', self.color_list)
        )

    def update(self):
        for cell in self.state_grid.updated:
            i = cell[0]
            j = cell[1]
            vertex_index = (self.state_grid.columns * 4 * i) + j * 4
            color_index = vertex_index * 3
            if self.state_grid.cells[i][j] == 1:
                self.vertex_list.colors[color_index:color_index+12] = [50, 50, 50]*4
            else:
                self.vertex_list.colors[color_index:color_index + 12] = [255, 255, 255] * 4
