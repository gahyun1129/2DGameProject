from pico2d import *

import server
import game_framework
import game_world

import module.make_team as make_team
import object.base as base


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            server.cur_pitcher.handle_event(event)


def init():
    game_world.add_object(server.background, 0)

    # 현재 모드에서의 공격 팀과 수비 팀 명시
    server.defence_team = make_team.user_players
    server.attack_team = make_team.computer_players

    # 공격 팀, 수비 팀 초기 위치 배치
    make_team.attack_position(server.attack_team)
    make_team.defence_position(server.defence_team)

    # 공격에 사용될 공 생성
    game_world.add_object(server.ball, 0)

    # ui 생성
    game_world.add_object(server.progress_bar, 3)

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
    game_world.update()
    game_world.handle_collisions()


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
    pass


def resume():
    pass
