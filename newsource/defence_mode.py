import game_framework
from pico2d import *
from ball import Ball
import make_team
import game_world

cur_hitter = None
out_count = 0
# goal_runner가 삭제될 때 점수 +1
goal_runner = None
my_ball = None


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            make_team.user_players[0].handle_event(event)


def init():
    global my_ball
    # 현재 모드에서의 공격 팀과 수비 팀 명시
    game_world.defence_team = make_team.user_players
    game_world.attack_team = make_team.computer_players

    # 공격 팀, 수비 팀 초기 위치 배치
    make_team.attack_position(game_world.attack_team)
    make_team.defence_position(game_world.defence_team)

    # 공격에 사용될 공 생성
    my_ball = Ball()
    game_world.add_object(my_ball, 0)

    # 수비수와 공의 충돌 설정
    game_world.add_collision_pair('ball:defender', my_ball, None)

    for defender in game_world.defence_team[2:9]:
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
