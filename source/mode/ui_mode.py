# init, handle_event, draw 등의 함수를 가진 모듈
# play scene == play mode, 작은 게임 루프...


from pico2d import *

import game_world
import server
import game_framework


# Game object class here


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_mode()  # 앞의 모드로 돌아감, 스택에서 가장 최근에 추가된 모드!


def init():
    game_world.add_object(server.ui_inning, 3)


def update():
    game_world.update()
    if server.ui_inning.x == 100:
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
