# 파일에서 플레이어 정보 읽어오고 팀을 만드는 모드
# 유저는 플레이어의 정보를 보고 자신의 팀을 구성한다.
# 팀 구성이 완료되면 Play 버튼을 누른다.

import game_framework
from pico2d import *

import game_make_team
import game_world

cur_hitter = None
out_count = 0
# goal_runner가 삭제될 때 점수 +1
goal_runner = None
ball = None


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
    # 데이터 읽어 오기
    game_make_team.set_player_from_data_file()
    # com 팀과 user 팀 선수 랜덤 으로 정하기
    game_make_team.make_team()
    # com 팀이 수비, user 팀이 공격인 위치로 배치 하기
    game_make_team.attack_position(game_make_team.user_players)
    game_make_team.defence_position(game_make_team.computer_players)
    game_world.add_object(ball, 3)

    game_world.add_collision_pair('ball:defender', ball, None)
    for defender in game_world.objects[1][2:9]:
        game_world.add_collision_pair('ball:defender', None, defender)


def update():
    game_world.update()
    game_world.handle_collisions()


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