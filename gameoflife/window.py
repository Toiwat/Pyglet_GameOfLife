import pyglet
import gameoflife as gol
from math import floor, fabs


class GameOfLife(pyglet.window.Window):
    def __init__(self, window_width=800, window_height=600, tile_size=32, time_interval=1/10, grid_size=(0, 0)):
        super(GameOfLife, self).__init__(width=window_width, height=window_height,
                                         resizable=False,
                                         caption="Game of Life - Running: False")

        if grid_size == (0, 0):
            grid_columns = (window_width-40) // tile_size
            grid_rows = (window_height-100) // tile_size
        else:
            grid_columns = grid_size[1]
            grid_rows = grid_size[0]

        self.width = window_width
        self.height = window_height

        self.state_grid = gol.grid.NumpyGrid(grid_rows, grid_columns)
        self.viewer = gol.viewer.PygletOpenglViewer(self.state_grid, self, tile_size=tile_size,
                                         color_dead=(255, 255, 255), color_alive=(100, 100, 100))

        self.time_interval = time_interval

        self.batch_labels = pyglet.graphics.Batch()
        self.label_generation = pyglet.text.Label("Generation: " + str(self.state_grid.generation),
                                                  font_name="Segoe UI",
                                                  font_size=16,
                                                  x=10, y=10,
                                                  batch=self.batch_labels)
        self.label_time_interval = pyglet.text.Label("Simulation Speed: " + str(self.time_interval) + " sec.",
                                                     font_name="Segoe UI",
                                                     font_size=16,
                                                     x=window_width-10, y=10,
                                                     anchor_x='right',
                                                     batch=self.batch_labels)
        self.label_instructions = pyglet.text.Label("Left click to draw cells, right click to erase.",
                                                    font_name="Segoe UI",
                                                    font_size=14,
                                                    x=10, y=window_height-10,
                                                    anchor_y='top',
                                                    batch=self.batch_labels)
        self.label_controls = pyglet.text.Label("Play/Pause: Space\nSimulation speed control: +/-",
                                                font_name="Segoe UI",
                                                font_size=10,
                                                x=window_width-10, y=window_height - 10,
                                                anchor_x='right', anchor_y='top',
                                                batch=self.batch_labels,
                                                multiline=True, width=200)

        self.running = False

    def set_time_interval(self):
        pyglet.clock.unschedule(self.update)
        pyglet.clock.schedule_interval(self.update, self.time_interval)
        self.label_time_interval.text = "Speed: " + str(self.time_interval) + " sec."

    def run(self):
        pyglet.clock.schedule_interval(self.update, self.time_interval)
        pyglet.app.run()

    def update(self, dt):
        if self.running:
            self.state_grid.update()
            self.viewer.update()

            self.label_generation.text = "Generation: " + str(self.state_grid.generation)

    def edit_cells(self, x, y, mouse_button):
        if self.viewer.is_position_inside_view_limits(x, y):
            cell_row = floor(fabs(self.viewer.top_left.y - y) // self.viewer.tile_size)
            cell_col = floor(fabs(self.viewer.top_left.x - x) // self.viewer.tile_size)

            if mouse_button == pyglet.window.mouse.LEFT:
                self.state_grid.set_cell_state(cell_row, cell_col, alive=True)
            elif mouse_button == pyglet.window.mouse.RIGHT:
                self.state_grid.set_cell_state(cell_row, cell_col, alive=False)

            self.viewer.update()

    def on_mouse_press(self, x, y, button, modifiers):
        self.edit_cells(x, y, button)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.edit_cells(x, y, buttons)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self.running = not self.running
            self.set_caption("Game of Life - Running: " + str(self.running))

        elif symbol == pyglet.window.key.PLUS:
            self.time_interval /= 2
            self.set_time_interval()
        elif symbol == pyglet.window.key.MINUS:
            self.time_interval *= 2
            self.set_time_interval()

    def on_draw(self):
        self.clear()
        self.viewer.batch.draw()
        self.batch_labels.draw()
