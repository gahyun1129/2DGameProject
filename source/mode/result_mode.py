# 게임 시작 시, 가장 처음 보이는 로고 모드
# 스페이스 바 누르면 게임이 시작됨.
# logo_mode > lobby_mode

import game_framework
from pico2d import *

import mode.lobby_mode as lobby_mode
import server


def init():
    global image
    image = load_image('resource/image/title.png')


def finish():
    server.out_count = 0
    server.cur_inning = 1
    server.cur_inning_turn = 0

    server.user_score = 0
    server.com_score = 0

    server.attack_team.clear()
    server.defence_team.clear()

    server.is_end = False
    server.cur_hitter = None
    server.cur_pitcher = None
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
            game_framework.change_mode(lobby_mode)


def pause():
    pass


def resume():
    pass
