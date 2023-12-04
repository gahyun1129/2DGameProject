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
import copy

import module.make_team as make_team
import object.background as background
import object.ball as ball
import ui.progress_bar as progress_bar
import ui.inning_ui as inning_ui
import ui.game_ment_ui as game_ment_ui
import ui.judge_ui as judge_ui
import ui.hitter_info_ui as hitter_info_ui
import ui.game_info_ui as game_info_ui
import ui.icon as icon
import ui.mini_map_ui as mini_map_ui
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
    server.ui_mini_map = mini_map_ui.MiniMapUI()

    # lobby_mode에서 할 일
    # object[0] : pitcher list, hitter list, icon
    # object[1] : user

    # 투수 목록 읽기
    server.team_element = [list_element.Element('투수', copy.copy(p)) for p in make_team.pitchers]

    for i in range((server.list_page - 1) * 4, server.list_page * 4):
        server.team_element[i].set_x_y(210, 430 - i * 100)
        game_world.add_object(server.team_element[i], 0)

    next_page_icon = icon.Icon('nextpage_icon', 'next_page', 250, 50)
    game_world.add_object(next_page_icon, 0)

    prev_page_icon = icon.Icon('prevpage_icon', 'prev_page', 150, 50)
    game_world.add_object(prev_page_icon, 0)

    team_list_ok_icon = icon.Icon('ok_icon', 'pitcher_ok', 350, 50)
    game_world.add_object(team_list_ok_icon, 0)

    user_next_page_icon = icon.Icon('nextpage_icon', 'user_next_page', 640, 50)
    game_world.add_object(user_next_page_icon, 0)

    user_prev_page_icon = icon.Icon('prevpage_icon', 'user_prev_page', 540, 50)
    game_world.add_object(user_prev_page_icon, 0)


def finish():
    # 게임 오브젝트 모두 삭제
    game_world.clear()
    game_world.clear_collision_pairs()

    server.selected_pitcher = None
    server.selected_hitter.clear()

    server.user_page = 1
    server.prev_user_page = 1
    server.list_page = 1
    server.prev_list_page = 1

    server.team_element.clear()
    server.user_team_element.clear()

    server.select_pitcher_num = 0
    server.select_hitter_num = 0
    server.bgm.stop()


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
        elif event.type == SDL_MOUSEBUTTONDOWN:
            for o in game_world.objects[0]:
                if game_world.collide_with_mouse(o, (event.x, 600 - 1 - event.y)):
                    o.handle_collide()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            make_team.make_auto_team()
            game_framework.change_mode(attack_mode)


def pause():
    pass


def resume():
    pass


def draw_list(elements, x):
    # 전 페이지 삭제
    for o in elements[(server.prev_list_page - 1) * 4:server.prev_list_page * 4]:
        game_world.remove_object(o)

    # 현 페이지 draw
    if len(elements) % 4 == 0:
        if server.list_page == len(elements) // 4 + 1:
            server.list_page = 1
        elif server.list_page == 0:
            server.prev_list_page = len(elements) // 4
            server.list_page = len(elements) // 4
    else:
        if server.list_page == len(elements) // 4 + 2:
            server.prev_list_page = 1
            server.list_page = 1
        if server.list_page == 0:
            server.prev_list_page = len(elements) // 4
            server.list_page = len(elements) // 4 + 1
    if len(elements) < 5:
        print('0')
        server.list_page = 1
        server.prev_list_page = 1

    i = 0
    for o in elements[(server.list_page - 1) * 4:server.list_page * 4]:
        o.set_x_y(x, 430 - (i % 4) * 100)
        game_world.add_object(o, 0)
        i += 1


def draw_list_user(elements, x):
    game_world.objects[1].clear()

    # 현 페이지 draw
    if len(elements) % 4 == 0:
        if server.user_page == len(elements) // 4 + 1:
            server.user_page = 1
        elif server.user_page == 0:
            server.prev_user_page = len(elements) // 4
            server.user_page = len(elements) // 4
    else:
        if server.user_page == len(elements) // 4 + 2:
            server.prev_user_page = 1
            server.user_page = 1
        if server.user_page == 0:
            server.prev_user_page = len(elements) // 4
            server.user_page = len(elements) // 4 + 1
    if len(elements) < 5:
        server.user_page = 1
        server.prev_user_page = 1

    i = 0
    for o in elements[(server.user_page - 1) * 4:server.user_page * 4]:
        o.set_x_y(x, 430 - (i % 4) * 100)
        game_world.add_object(o, 1)
        i += 1
