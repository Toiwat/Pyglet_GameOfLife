import timeit

if __name__ == "__main__":
    sprite_time = []
    sprite_np_time = []
    ogl_time = []

    cycles = 10
    grid_size = 500

    print("Timing first set...")
    sprite_time.append(timeit.timeit(stmt="sprites.update(state)",
                                setup='from game.grid.array_grid import ArrayGrid; \
                                from game.ui.spritegrid import PygletSpritesViewer; \
                                state = ArrayGrid(' + str(grid_size) + ', ' + str(grid_size) + '); \
                                sprites = PygletSpritesViewer(state, 1280, 720)', number=cycles))

    print("Timing second set...")
    sprite_np_time.append(timeit.timeit(stmt="sprites.update(state)",
                                     setup='from game.grid.array_grid import NumpyGrid; \
                                    from game.ui.spritegrid import PygletSpritesViewer; \
                                    state = NumpyGrid(' + str(grid_size) + ', ' + str(grid_size) + '); \
                                    sprites = PygletSpritesViewer(state, 1280, 720)', number=cycles))

    print("Timing third set...")
    ogl_time.append(timeit.timeit(stmt="grid.update(state)",
                                   setup='from game.grid.array_grid import NumpyGrid; \
                                    from game.ui.gl_renderer import PygletOpenglViewer; \
                                    state = NumpyGrid(' + str(grid_size) + ', ' + str(grid_size) + '); \
                                    grid = PygletOpenglViewer(state, 1280, 720, 16)', number=cycles))

    print("\n Tests finished!")
    print("--- Average run time over " + str(cycles) + " cycles, "
                                                       "grid size " + str(grid_size) + "x" + str(grid_size) + " ---")
    print("v. 0.1: Original (Sprites + python arrays): " + str(sum(sprite_time)/cycles))
    print("v. 0.2: Sprite-based UI with Numpy representation: " + str(sum(sprite_np_time) / cycles))
    print("v. 0.4: Numpy + optimized OpenGL: " + str(sum(ogl_time)/cycles))
