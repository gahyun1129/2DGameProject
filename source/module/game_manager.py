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


class GameManager:
    def __init__(self):
        # 1이닝부터 9이닝까지 한 게임에 관련한 데이터
        self.cur_inning = 1
        self.cur_inning_turn = 0

        self.user_score = 0
        self.com_score = 0

        # 한 이닝에 관련한 데이터
        self.out_count = 0

        self.cur_hitter = None
        self.cur_pitcher = None

        self.state = None

    def set_next_hitter(self, hitter):
        hitter.out_sound.play()
        hitter.strike, hitter.ball = 0, 0
        hitter.base.has_runner = False
        make_team.search_next_hitter(hitter)
        game_world.remove_object(hitter)
        if self.out_count == 3:
            self.out_situation()

    def out_situation(self):
        self.out_count = 0
        self.cur_inning_turn = (self.cur_inning_turn + 1) % 2  # turn = 0: attack_mode, 초 turn = 1: defence_mode, 말
        if self.cur_inning_turn == 0:
            self.cur_inning += 1
        if self.cur_inning == 10:
            server.game_status = 'end'
            print('게임 끝!!!!!!!')
        else:
            server.ui_inning.frame = self.cur_inning - 1
            server.ui_inning.size = 1
            if self.cur_inning_turn == 0:
                server.ui_inning.turn = 3
                game_framework.change_mode(attack_mode)
                server.ui_hitter_info.hitter_image = load_image('resource/image/hitter_red.png')
            else:
                server.ui_inning.turn = 2
                game_framework.change_mode(defence_mode)
                server.ui_hitter_info.hitter_image = load_image('resource/image/hitter_blue.png')

    def set_ui(self):
        server.progress_bar.frame = 0
        server.progress_bar.action = 0
        server.progress_bar.is_hit = False
        server.ui_ball_icon.is_draw = True
        server.ui_strike_icon.is_draw = True

    # hitter의 hit이 끝났고, 수비수의 수비가 끝났을 때
    def update(self):
        match self.state:
            case 'ball':
                server.ui_ment.draw_ment_ui('ball', self.cur_hitter.ball)  # ball ui 출력
                self.cur_hitter.catch_sound.play()
                self.cur_hitter.state_machine.handle_event(('HIT_FAIL', 0))
                self.state = 'set_next'
                pass
            case 'strike':
                server.ui_ment.draw_ment_ui('strike', self.cur_hitter.strike)  # strike ui 출력
                self.cur_hitter.catch_sound.play()
                self.cur_hitter.state_machine.handle_event(('HIT_FAIL', 0))
                self.state = 'set_next'
                pass
            case 'four_ball':
                server.ui_ment.draw_ment_ui('ball', self.cur_hitter.ball)  # ball ui 출력
                self.cur_hitter.catch_sound.play()
                self.cur_hitter.strike, self.cur_hitter.ball = 0, 0
                for runner in game_world.objects[2]:
                    runner.state_machine.handle_event(('FOUR_BALL', 0))  # 타자와 주자는 1루를 향해 뜀
                self.state = None
                # 다음 타자 생성
                # server.ui_ment.draw_ment_ui('ball', self.cur_hitter.ball)  # ball ui 출력
                # self.cur_hitter.catch_sound.play()
                pass
            case '3strike':
                print('3strike')
                server.ui_ment.draw_ment_ui('strike', self.cur_hitter.strike)  # strike ui 출력
                self.cur_hitter.catch_sound.play()
                self.out_count += 1
                server.ui_judge.draw_judge_ui('out', self.out_count)
                self.set_next_hitter(self.cur_hitter)
                self.state = 'set_next'
                pass
            case 'safe':
                server.ui_judge.draw_judge_ui('safe')
                server.ball.state_machine.handle_event(('BACK_TO_MOUND', 0))
                for o in game_world.objects[1][2:9]:
                    if o.pos is not o.defence_position:
                        print('돌아감', o.name)
                        o.state_machine.handle_event(('BACK_TO_DEFENCE', 0))
                self.state = 'set_hitter'
                pass
            case 'out':
                self.out_count += 1
                server.ui_judge.draw_judge_ui('out', self.out_count)
                self.set_next_hitter(self.cur_hitter)
                server.ball.state_machine.handle_event(('BACK_TO_MOUND', 0))
                # 수비수 (투수, 포수 제외)
                for o in game_world.objects[1][2:9]:
                    if o.pos is not o.defence_position:
                        print('돌아감', o.name)
                        o.state_machine.handle_event(('BACK_TO_DEFENCE', 0))
                self.state = None
                pass
            case 'set_hitter':
                make_team.search_next_hitter(self.cur_hitter)
                self.state = 'set_next'
                pass
            case 'set_next':
                self.set_ui()
                self.state = None
                pass
