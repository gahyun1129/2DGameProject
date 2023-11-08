import game_framework
from pico2d import *

import make_team
import game_world
from ball import Ball

cur_hitter = None
current_event = ('None', 0)
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
            make_team.computer_players[0].handle_event(event)


def init():
    # 데이터 읽어 오기
    make_team.set_player_from_data_file()
    # com 팀과 user 팀 선수 랜덤 으로 정하기
    make_team.make_team()
    # com 팀이 수비, user 팀이 공격인 위치로 배치 하기
    make_team.attack_position(make_team.user_players)
    make_team.defence_position(make_team.computer_players)
    game_world.add_object(ball, 3)


def update():
    game_world.update()


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
