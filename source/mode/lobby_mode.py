# lobby_mode > attack_mode 해결
# 파일에서 선수 명단 읽어 오기  해결
#####################################
# user 팀 선정하기           해야 함...
#####################################
# ui랑 ball, base 초기화하기  해결

from pico2d import *

import game_world
import server
import game_framework

import module.make_team as make_team
import object.background as background
import object.ball as ball
import ui.progress_bar as progress_bar
import ui.inning_ui as inning_ui
import ui.game_ment_ui as game_ment_ui
import ui.judge_ui as judge_ui
import ui.hitter_info_ui as hitter_info_ui
import ui.game_info_ui as game_info_ui

import module.list_element as list_element

import mode.attack_mode as attack_mode


def init():
    global background_image
    background_image = load_image('resource/image/lobby.png')

    # 데이터 읽어 오기
    make_team.set_player_from_data_file()

    # com 팀과 user 팀 선수 랜덤 으로 정하기
    make_team.make_team()

    # 공격에 사용될 공 생성
    server.background = background.Background()
    server.ball = ball.Ball()

    # ui 생성
    server.progress_bar = progress_bar.ProgressBar()
    server.ui_ment = game_ment_ui.MentUI()
    server.ui_inning = inning_ui.InningUI()
    server.ui_judge = judge_ui.JudgeUI()
    server.ui_hitter_info = hitter_info_ui.HitterInfoUI()
    server.ui_game_info = game_info_ui.GameInfoUI()

    # lobby_mode에서 할 일

    # 투수 목록 읽기
    elements = [list_element.Element('투수', p) for p in make_team.pitchers]

    list_start = 0
    list_end = 4

    for x in range(list_start, list_end):
        elements[x].set_x_y(210, 430 - x * 100)
        game_world.add_object(elements[x], 2)



def finish():
    # 게임 오브젝트 모두 삭제
    game_world.clear()
    game_world.clear_collision_pairs()


def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    background_image.draw(400, 300)
    game_world.render()
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
