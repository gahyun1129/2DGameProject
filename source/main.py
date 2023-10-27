from pico2d import *
from Player import Pitcher


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            pitcher.handle_events(event)


def create_world():
    global running
    global pitcher

    running = True

    pitcher = Pitcher()


def update_world():
    pitcher.update()


def render_world():
    clear_canvas()
    pitcher.render()
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