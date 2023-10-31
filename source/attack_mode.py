# 게임 play 중 attack_mode
# 공격: 파란 팀, 수비: 빨간 팀
# 파란 팀을 주인공으로 진행함

from pico2d import *
import game_framework

import game_world
from player import Pitcher, Hitter



def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        # else:
            # pitcher.handle_events(event)


def create_world():
    global hitter
    global pitcher

    game_world.set_player_list_from_data_file()

    hitter = game_world.hitter_player[0]
    pitcher = game_world.pitcher_player[0]
    print(hitter.name)
    print(pitcher.name)


def update_world():
    pitcher.update()
    hitter.update()


def render_world():
    clear_canvas()
    pitcher.render()
    hitter.render()
    update_canvas()


