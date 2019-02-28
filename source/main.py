import pyglet
from game.window import GameOfLife


if __name__ == "__main__":
    window = GameOfLife()

    pyglet.clock.schedule_interval(window.update, 1/10)
    pyglet.app.run()
