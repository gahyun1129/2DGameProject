# 게임 시작 시, 가장 처음 보이는 로고 모드
# 스페이스 바 누르면 게임이 시작됨.
# logo_mode > lobby_mode

import game_framework
from pico2d import *

import game_world
import mode.lobby_mode as lobby_mode
import server
import ui.icon as icon


def init():
    global image
    global main_ui, retry_icon, exit_ui
    image = load_image('resource/image/result.png')
    main_ui = icon.Icon('info', 'main', 400, 300, 800, 600)
    game_world.add_object(main_ui, 3)

    exit_ui = icon.Icon('exit_icon', 'exit', 400, 200, 380, 70)
    game_world.add_object(exit_ui, 4)

    retry_icon = icon.Icon('retry_icon', 'retry', 400, 400, 380, 70)
    game_world.add_object(retry_icon, 4)


def finish():
    game_world.remove_object(main_ui)
    game_world.remove_object(retry_icon)
    game_world.remove_object(exit_ui)
    server.bgm.repeat_play()


def update():
    pass


def draw():
    clear_canvas()
    image.draw(400, 300)
    game_world.render()
    update_canvas()
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_mode()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            for o in game_world.objects[4]:
                if game_world.collide_with_mouse(o, (event.x, 600 - 1 - event.y)):
                    o.handle_collide()


def pause():
    pass


def resume():
    pass
