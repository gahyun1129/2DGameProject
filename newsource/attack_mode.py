import game_framework
from pico2d import *

from hitter import Hitter
from pitcher import Pitcher
import make_team


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()


def init():
    global pitcher
    global hitter

    make_team.set_player_from_data_file()

    pitcher = make_team.pitchers[0]
    hitter = make_team.hitters[0]


def update():
    pitcher.update()
    hitter.update()


def draw():
    clear_canvas()
    pitcher.draw()
    hitter.draw()
    update_canvas()


def finish():
    pass


def pause():
    pass


def resume():
    pass