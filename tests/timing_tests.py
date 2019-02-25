import pyglet
from game.stategrid import StateGrid
from game.stategrid_np import StateGridNP
import timeit

if __name__ == "__main__":

    n = 100

    state = StateGrid(n, n)
    npstate = StateGridNP(n, n)
    state_time = timeit.timeit(state.update, number=1000)
    npstate_time = timeit.timeit(npstate.update, number=1000)
    sprite_time = timeit.timeit(stmt="sprites.update(state)",
                                setup='from game.stategrid import StateGrid; \
                                from game.spritegrid import SpriteGrid; \
                                state = StateGrid(100, 100); \
                                sprites = SpriteGrid(state, 1280, 720)', number=1000)

    print("State grid updates, size " + str(n) + " x " + str(n) +" (1000 cycles): " + str(state_time))
    print("State grid updates, size " + str(n) + " x " + str(n) +" (1000 cycles): " + str(npstate_time))
    print("Sprite grid updates, size " + str(n) + " x " + str(n) +" (1000 cycles): : " + str(sprite_time))

    pyglet.app.run()
