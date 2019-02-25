import pyglet
from game.window import GameOfLife


if __name__ == "__main__":
    window = GameOfLife(1280, 720, 40, 60)

    pyglet.clock.schedule_interval(window.update, 1/10)
    pyglet.app.run()
