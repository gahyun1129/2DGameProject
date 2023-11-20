import define
import game_framework
from pico2d import *

import game_make_team
import game_world
from object_grass import Grass
from object_ui import UI
from player_ball import Ball

cur_hitter = None
out_count = 0
# goal_runner가 삭제될 때 점수 +1
goal_runner = None
my_ball = None
make_ui = None
make_ui2 = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            game_make_team.computer_players[0].handle_event(event)


def init():
    global my_ball
    global make_ui
    global make_ui2

    grass = Grass()
    game_world.add_object(grass, 0)

    # 데이터 읽어 오기
    game_make_team.set_player_from_data_file()

    # com 팀과 user 팀 선수 랜덤 으로 정하기
    game_make_team.make_team()

    # 현재 모드에서의 공격 팀과 수비 팀 명시
    game_world.defence_team = game_make_team.computer_players
    game_world.attack_team = game_make_team.user_players

    # set base
    define.set_base()

    # 공격 팀, 수비 팀 초기 위치 배치
    game_make_team.attack_position(game_world.attack_team)
    game_make_team.defence_position(game_world.defence_team)

    # 공격에 사용될 공 생성
    my_ball = Ball()
    game_world.add_object(my_ball, 0)

    # UI 그림
    make_ui = UI()
    game_world.add_object(make_ui, 3)

    # 수비수와 공의 충돌 설정
    # 수비수와 base 충돌 설정
    # hitter와 base 충돌 설정

    game_world.add_collision_pair('ball:defender', my_ball, None)
    for base in define.bases:
        game_world.add_collision_pair('base:defender', base, None)
        game_world.add_collision_pair('hitter:base', None, base)

    for defender in game_world.defence_team[2:9]:
        game_world.add_collision_pair('ball:defender', None, defender)
        game_world.add_collision_pair('base:defender', None, defender)
    game_world.add_collision_pair('base:defender', None, game_world.defence_team[1])


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
