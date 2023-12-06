from pico2d import load_image, load_font, draw_rectangle, load_music, load_wav

import game_framework
import server
import random

import mode.result_mode as result_mode
import mode.attack_mode as attack_mode
import mode.defence_mode as defence_mode
import module.make_team as make_team
import object.ball as obj_ball
from object.base import *


def set_next_hitter(hitter):
    hitter.out_sound.play()
    hitter.strike, hitter.ball = 0, 0
    hitter.base.has_runner = False
    make_team.search_next_hitter(server.cur_hitter)
    game_world.remove_object(hitter)
    if server.out_count == 3:
        out_situation()


def out_situation():
    server.out_count = 0
    server.cur_inning_turn = (server.cur_inning_turn + 1) % 2  # turn = 0: attack_mode, 초 turn = 1: defence_mode, 말
    if server.cur_inning_turn == 0:
        server.cur_inning += 1
    if server.cur_inning == 10:
        server.game_status = 'end'
        print('게임 끝!!!!!!!')
        # game_framework.change_mode(result_mode)
        # 나중에 여기서 결과 모드로 바꾸면 될 듯
    else:
        server.ui_inning.frame = server.cur_inning - 1
        server.ui_inning.size = 1
        if server.cur_inning_turn == 0:
            server.ui_inning.turn = 3
            game_framework.change_mode(attack_mode)
            server.ui_hitter_info.hitter_image = load_image('resource/image/hitter_red.png')
        else:
            server.ui_inning.turn = 2
            game_framework.change_mode(defence_mode)
            server.ui_hitter_info.hitter_image = load_image('resource/image/hitter_blue.png')


class GameManager:
    def __init__(self):
        # 1이닝부터 9이닝까지 한 게임에 관련한 데이터
        self.cur_inning = 1
        self.cur_inning_turn = 0

        self.user_score = 0
        self.team_score = 0

        self.attack_team = None
        self.defence_team = None

        # 한 이닝에 관련한 데이터
        self.out_count = False

        self.cur_hitter = None
        self.cur_pitcher = None

        self.run_end = False
        self.defence_end = False
        self.hitter_run_end = False

        self.need_to_set_next_hitter = False

    # hitter의 hit이 끝났고, 수비수의 수비가 끝났을 때
    def update(self):
        if self.run_end and self.defence_end:
            print("hit")
            server.progress_bar.frame = 0
            server.progress_bar.action = 0
            server.progress_bar.is_hit = False
            server.ui_ball_icon.is_draw = True
            server.ui_strike_icon.is_draw = True
            if self.need_to_set_next_hitter:
                set_next_hitter(server.cur_hitter)
            self.run_end, self.defence_end = False, False
            self.need_to_set_next_hitter = False
