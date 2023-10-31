# 게임 play 중 attack_mode
# 공격: 파란 팀, 수비: 빨간 팀
# 파란 팀을 주인공으로 진행함

from pico2d import *
import game_framework

import game_world
from player import Pitcher, Hitter


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        # else:
            # pitcher.handle_events(event)


def init():
    global hitter
    global pitcher
    
    game_world.set_player_list_from_data_file()

    # hitter = game_world.hitter_player[0]
    # pitcher = game_world.pitcher_player[0]
    # print(hitter.name)
    # print(pitcher.name)


def update():
    game_world.update()
    # pitcher.update()
    # hitter.update()


def draw():
    clear_canvas()
    game_world.render()
    # pitcher.render()
    # hitter.render()
    update_canvas()


def finish():
    game_world.clear()
    pass


def pause():
    pass


def resume():
    pass