from gameoflife.window import GameOfLife


if __name__ == "__main__":
    window = GameOfLife(window_width=1280, window_height=720, tile_size=16)
    window.run()


