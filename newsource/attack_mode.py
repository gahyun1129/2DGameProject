import game_framework
from pico2d import *


import make_team
import game_world
from define import *

cur_hitter = None
current_event = ('None', 0)
# goal_runner가 삭제될 때 점수 +1
goal_runner = None


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            cur_hitter.handle_event(event)


def init():
    make_team.set_player_from_data_file()
    make_team.make_team()
    make_team.attack_position()


def update():
    global cur_hitter
    global current_event
    global goal_runner

    game_world.update()

    # 타자가 hit을 성공한 후 1루수로 달리고 난 경우
    # 다음 순서로 타자 변경, 현재 타자는 주루 플레이어로 상태 머신 업데이트
    # 목표로 하는 position이 home인 경우, home으로 도착 후 타자 객체 game_world에서 삭제
    if current_event[0] == 'RUN_DONE':
        next_hitter = make_team.user_players[make_team.user_players.index(cur_hitter)+1 % 9]
        cur_hitter.set_runner_state_machine()
        cur_hitter = next_hitter
        cur_hitter.pos = attack_zone
        cur_hitter.init_state_machine()
        game_world.add_object(cur_hitter, 2)
        current_event = ('None', 0)
        if goal_runner is not None:
            game_world.remove_object(goal_runner)
            goal_runner = None

    # 현재 타자가 hit을 성공한 경우, 주루 플레이어들은 달림
    if current_event[0] == 'HIT_SUCCESS':
        game_world.update_handle_event()
        current_event = ('None', 0)

    # 현재 타자가 hit을 실패한 경우, 현재 타자 삭제 및 다음 타자 불러옴
    if current_event[0] == 'HIT_DONE':
        next_hitter = make_team.user_players[make_team.user_players.index(cur_hitter) + 1 % 9]
        print(next_hitter.name, cur_hitter.name)
        game_world.remove_object(cur_hitter)
        cur_hitter = next_hitter
        cur_hitter.pos = attack_zone
        cur_hitter.init_state_machine()
        game_world.add_object(cur_hitter, 2)
        current_event = ('None', 0)


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