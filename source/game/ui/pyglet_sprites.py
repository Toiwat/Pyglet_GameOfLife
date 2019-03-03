from pyglet.sprite import Sprite
from game.grid.stategrid import StateGrid
from game import resources
from game.ui._base_viewer import Viewer


class PygletSpritesViewer(Viewer):
    def __init__(self, state_grid: StateGrid, window, color_dead=(255, 255, 255), color_alive=(50,50,50)):
        # List for pyglet sprites
        self.sprites = []
        super(PygletSpritesViewer, self).__init__(state_grid, window, tile_size=16, color_alive=color_alive, color_dead=color_dead)

    def setup(self):
        self.sprites = [[Sprite(img=resources.x16_with_border,
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
