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


def init():
    make_team.set_player_from_data_file()
    make_team.make_team()
    make_team.attack_position()


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