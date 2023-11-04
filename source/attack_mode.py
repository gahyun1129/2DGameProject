# 게임 play 중 attack_mode
# 공격: 파란 팀, 수비: 빨간 팀
# 파란 팀을 주인공으로 진행함

from pico2d import *
from define import *
import game_framework

import game_world
import make_team
import player


cur_hitter = None


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
    global cur_hitter
    # 팀을 구성하고
    make_team.set_player_list_from_data_file()

    # 위치 잡고
    player.defence_position(make_team.com_players)
    cur_hitter = make_team.user_players[1]
    (cur_hitter.x, cur_hitter.y) = attack_zone


    # 그려질 객체 추가하기
    game_world.add_objects(make_team.com_players, 0)
    game_world.add_object(cur_hitter, 1)

    print(game_world.objects)


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()
    pass


def pause():
    pass


def resume():
    pass


###########################################################################
# 1) 선수들 배치하기 - clear
# 2) 투수의 공 던지기
# 3) 타자의 히트 타이밍 재는 UI 내보내기
# 4) 히트 타이밍 * OPS * 안타율 해서 히트 성공/실패 여부 따지기
# 5-1) 성공 > 타자 달리기
# 5-2) 실패 > 스트라이크 포인트 올리기
# 6) 3아웃까지 무한 반복!
