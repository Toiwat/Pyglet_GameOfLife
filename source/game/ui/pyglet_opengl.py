from pyglet.gl import GL_QUADS
from game.grid.stategrid import StateGrid
from game.ui._base_viewer import Viewer


class PygletOpenglViewer(Viewer):
    def __init__(self, state_grid: StateGrid, window, tile_size=16, color_dead=(255, 255, 255), color_alive=(50,50,50)):
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
            GL_QUADS,
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
