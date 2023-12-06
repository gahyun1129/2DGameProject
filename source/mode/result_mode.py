# 게임 시작 시, 가장 처음 보이는 로고 모드
# 스페이스 바 누르면 게임이 시작됨.
# logo_mode > lobby_mode

import game_framework
from pico2d import *

import game_world
import mode.lobby_mode as lobby_mode
import mode.esc_mode as esc_mode
import server
import ui.icon as icon


def init():
    global image
    global font
    global main_ui

    game_world.clear()

    image = load_image('resource/image/result.png')
    font = load_font('resource/txt/DungGeunMo.TTF', 180)


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

    server.game_status = None
    pass


def update():
    if server.game_status == 'quit':
        game_framework.quit()


def draw():
    clear_canvas()
    image.draw(400, 300)
    font.draw(200, 180, f'{server.user_score}', (0, 0, 0))
    font.draw(520, 180, f'{server.com_score}', (0, 0, 0))
    if server.user_score > server.com_score:
        font.draw(100, 420, f'victory', (0, 0, 0))
    elif server.user_score < server.com_score:
        font.draw(220, 420, f'lose', (0, 0, 0))
    else:
        font.draw(220, 420, f'draw', (0, 0, 0))
    update_canvas()
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.push_mode(esc_mode)


def pause():
    pass


def resume():
    pass
