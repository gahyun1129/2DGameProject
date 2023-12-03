from pico2d import *

import server
import game_framework
import game_world
import mode.ui_mode as ui_mode

import mode.result_mode as result_mode
import module.make_team as make_team
import mode.play_esc_mode as play_esc_mode
import object.base as base


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.push_mode(play_esc_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_q:
            game_framework.change_mode(result_mode)
        else:
            server.cur_pitcher.handle_event(event)


def init():
    game_framework.push_mode(ui_mode)

    server.ui_ment.is_draw = False
    server.ui_ment.is_draw_number = False
    server.ui_judge.is_draw = False
    server.ui_judge.is_draw_number = False

    game_world.add_object(server.background, 0)

    # 현재 모드에서의 공격 팀과 수비 팀 명시
    server.defence_team = make_team.computer_players
    server.attack_team = make_team.user_players

    # 공격 팀, 수비 팀 초기 위치 배치
    make_team.attack_position(server.attack_team)
    make_team.defence_position(server.defence_team)

    # game_world에 객체 넣기
    game_world.add_object(server.ball, 0)
    game_world.add_object(server.ui_ment, 3)
    # game_world.add_object(server.progress_bar, 3)
    game_world.add_object(server.ui_judge, 3)

    # 수비수와 공의 충돌 설정
    # 수비수와 base 충돌 설정
    # hitter와 base 충돌 설정

    game_world.add_collision_pair('ball:defender', server.ball, None)
    for b in base.bases:
        game_world.add_collision_pair('base:defender', b, None)
        game_world.add_collision_pair('hitter:base', None, b)

    for defender in server.defence_team[2:9]:
        game_world.add_collision_pair('ball:defender', None, defender)
        game_world.add_collision_pair('base:defender', None, defender)
    game_world.add_collision_pair('base:defender', None, server.defence_team[1])


def update():
    game_world.handle_collisions()
    game_world.update()
    match server.game_status:
        case 'end':
            server.game_status = None
            game_framework.change_mode(result_mode)
        case 'stop':
            server.game_status = None
            game_framework.change_mode(result_mode)
        case 'quit':
            game_framework.quit()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    # 게임 오브젝트 모두 삭제
    game_world.clear()
    game_world.clear_collision_pairs()
    pass


def pause():
    server.ui_inning.x, server.ui_inning.y = 1000, 500


def resume():
    game_world.add_object(server.ui_hitter_info, 3)
    game_world.add_object(server.ui_game_info, 3)
    game_world.add_object(server.progress_bar, 3)
