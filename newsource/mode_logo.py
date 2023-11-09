# 게임 시작 시, 가장 처음 보이는 로고 모드
# 스페이스 바 누르면 게임이 시작됨.
# logo_mode > lobby_mode

import game_framework
from pico2d import *

import mode_attack


def init():
    global image
    image = load_image('resource/image/title.png')


def finish():
    pass


def update():
    pass


def draw():
    clear_canvas()
    image.draw(400, 300)
    update_canvas()
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_mode(mode_attack)


def pause():
    pass


def resume():
    pass
