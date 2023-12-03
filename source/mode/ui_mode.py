from pico2d import *

import game_world
import server
import game_framework


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()


def init():
    game_world.add_object(server.ui_inning, 4)


def update():
    game_world.update()
    if server.ui_inning.x == 110:
        game_framework.pop_mode()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    pass


def pause():
    pass


def resume():
    pass
