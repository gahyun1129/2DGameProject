import game_framework
from pico2d import *

from hitter import Hitter
from pitcher import Pitcher


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

    pitcher = Pitcher(300, 100, 0, 1, 0, 0, '박가현', 0, 0, 0, ['e', 'f'])
    hitter = Hitter(600, 100, 0, 1, 4, 1, '박가현', 0, 0, 0, 0, 0)


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