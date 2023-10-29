from pico2d import *
from player import Pitcher, Hitter
import game_world


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        # else:
            # pitcher.handle_events(event)


def create_world():
    global running
    global hitter
    global pitcher

    running = True

    # pitcher = Pitcher()
    # hitter = Hitter(400, 70, 0, 0, 6, 0, 0, 0, 0, 0, 0)
    game_world.init()

    hitter = game_world.hitter_player[0]
    print(hitter.name)


def update_world():
    # pitcher.update()
    hitter.update()


def render_world():
    clear_canvas()
    # pitcher.render()
    hitter.render()
    update_canvas()


open_canvas()
create_world()


# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.2)
# finalization code
close_canvas()