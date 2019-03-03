from pyglet.graphics import Batch
from collections import namedtuple
from game.grid.stategrid import StateGrid

Coord = namedtuple("Coord", "x y")


class Viewer:
    def __init__(self, state_grid: StateGrid, window, tile_size, color_dead, color_alive):

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
        self.batch = Batch()

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