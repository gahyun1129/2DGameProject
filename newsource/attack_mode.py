import game_framework
from pico2d import *

import make_team
import game_world

cur_hitter = None


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            cur_hitter.handle_event(event)

def init():
    make_team.set_player_from_data_file()
    make_team.make_team()
    make_team.attack_position()

    # for la in game_world.objects:
    #     for o in la:
    #         print(o.x, o.y)

def update():
    game_world.update()


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