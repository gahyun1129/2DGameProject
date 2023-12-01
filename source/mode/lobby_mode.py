# lobby_mode > attack_mode 해결
# 파일에서 선수 명단 읽어 오기  해결
#####################################
# user 팀 선정하기           해야 함...
#####################################
# ui랑 ball, base 초기화하기  해결

from pico2d import *

import server
import game_framework

import module.make_team as make_team
import object.ball as ball
import ui.progress_bar as progress_bar
import ui.inning_ui as inning_ui
import ui.game_ment_ui as game_ment_ui
import ui.judge_ui as judge_ui

import mode.attack_mode as attack_mode


def init():
    global image
    image = load_image('resource/image/lobby.png')

    # 데이터 읽어 오기
    make_team.set_player_from_data_file()

    # com 팀과 user 팀 선수 랜덤 으로 정하기
    make_team.make_team()

    # 공격에 사용될 공 생성
    server.ball = ball.Ball()

    # ui 생성
    server.progress_bar = progress_bar.ProgressBar()
    server.ui_ment = game_ment_ui.MentUI()
    server.ui_inning = inning_ui.InningUI()
    server.ui_judge = judge_ui.JudgeUI()


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
            game_framework.change_mode(attack_mode)


def pause():
    pass


def resume():
    pass
