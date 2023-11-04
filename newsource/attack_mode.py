import game_framework
from pico2d import *


import make_team
import game_world
from define import *

cur_hitter = None
current_event = ('None', 0)

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

    # for la in game_world.objects:
    #     for o in la:
    #         print(o.x, o.y)


def update():
    global cur_hitter
    global current_event

    game_world.update()
    
    if current_event[0] == 'RUN_DONE':
        next_hitter = make_team.user_players[make_team.user_players.index(cur_hitter)+1 % 9]
        cur_hitter.set_runner_state_machine()
        cur_hitter = next_hitter
        cur_hitter.pos = attack_zone
        cur_hitter.init_state_machine()
        game_world.add_object(cur_hitter, 2)
        current_event = ('None', 0)

    if current_event[0] == 'HIT_SUCCESS':
        print('HIT_SUCCESS')
        game_world.update_handle_event()
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