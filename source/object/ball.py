from pico2d import load_image, draw_rectangle
from object.base import *

import game_framework
import server
import game_world

import module.make_team as make_team
import mode.defence_mode as defence_mode
import random

import object.hitter as hitter

PIXEL_PER_METER = (10.0 / 0.3)


def throw_start(e):
    return e[0] == 'THROW_START'


def hit_success(e):
    return e[0] == 'HIT_SUCCESS'


def back_to_mound(e):
    return e[0] == 'BACK_TO_MOUND'


def throw_to_base(e):
    return e[0] == 'THROW_TO_BASE'


def throw_done(e):
    return e[0] == 'THROW_DONE'


def defender_catch(e):
    return e[0] == 'DEFENDER_CATCH'


class Throw:
    @staticmethod
    def enter(ball, e):
        ball.frame, ball.frame_number = 0, 1
        ball.event = e[0]

        # 투수가 공을 던지는 경우
        if e[0] == 'THROW_START':
            ball.pos = mound
            ball.goal_position = home

        # 타자가 공을 친 경우
        elif e[0] == 'HIT_SUCCESS':
            ball.pos = home
            x = random.randint(100, 900)
            y = random.randint(300, 800)
            ball.goal_position = (x, y)
        # 공이 다시 마운드, 투수에게로 돌아가는 상황
        elif e[0] == 'BACK_TO_MOUND':
            ball.goal_position = mound
        # 가장 가까운 주자가 있는 base 공을 던지는 경우 (수비)
        elif e[0] == 'THROW_TO_BASE':
            ball.goal_position = e[1].throw_to_base()
            print('e[1].throw_to_base(), 가까운 베이스로 던지기')
            pass
        ball.current_position = ball.pos
        ball.t = 0.0

    @staticmethod
    def exit(ball, e):
        # if my_ball.event == 'BACK_TO_MOUND':
        #     hitter = server.cur_hitter
        #     make_team.set_next_hitter(hitter)
        if ball.event == 'THROW_TO_BASE':
            if number_to_bases[ball.goal_position].hasDefender and not number_to_bases[ball.goal_position].hasRunner:
                print('ball done')
                hitter = server.cur_hitter
                hitter.strike, hitter.my_ball = 0, 0
                make_team.set_next_hitter(hitter)
                game_world.remove_object(hitter)
                server.out_count += 1
                if server.out_count == 3:
                    game_framework.change_mode(defence_mode)
        pass

    @staticmethod
    def do(ball):
        ball.frame = (ball.frame + 1) % ball.frame_number

        x = (1 - ball.t) * ball.current_position[0] + ball.t * ball.goal_position[0]
        y = (1 - ball.t) * ball.current_position[1] + ball.t * ball.goal_position[1]
        ball.pos = (x, y)

        ball.t += 0.1 * ((ball.RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * PIXEL_PER_METER * game_framework.frame_time

        # 목표 위치에 도착한 경우!!
        if ball.t > 1:
            # 마지막 위치 확실히 하기
            ball.pos = ball.goal_position
            ball.state_machine.handle_event(('THROW_DONE', 0))

    @staticmethod
    def draw(ball):
        sx, sy = ball.pos[0] - server.background.window_left, ball.pos[1] - server.background.window_bottom
        ball.image.clip_draw(ball.frame * 50, 0, 50, 50, sx, sy, 20, 20)


class Idle:
    @staticmethod
    def enter(ball, e):
        ball.event = e[0]
        if e[0] == 'DEFENDER_CATCH':
            # 타자 삭제
            hitter = server.cur_hitter
            hitter.strike, hitter.my_ball = 0, 0
            make_team.set_next_hitter(hitter)
            game_world.remove_object(hitter)
            ball.state_machine.handle_event(('BACK_TO_MOUND', 0))
            for player in server.defence_team[1:9]:
                player.state_machine.handle_event(('RUN_DONE', 0))
            # 수비수가 공 잡으려고 달리는 것도 멈춰야 함.
            print('한 번에 잡음')
        if e[0] == 'THROW_TO_BASE':
            ball.goal_position = e[1].throw_to_base()
        if ball.pos != mound and ball.is_collision:
            ball.state_machine.handle_event(('BACK_TO_MOUND', 0))

    @staticmethod
    def exit(ball, e):
        if ball.event == 'THROW_TO_BASE':
            if number_to_bases[ball.goal_position].hasDefender and not number_to_bases[ball.goal_position].hasRunner:
                print('ball done')
                hitter = server.cur_hitter
                hitter.strike, hitter.my_ball = 0, 0
                make_team.set_next_hitter(hitter)
                game_world.remove_object(hitter)
                server.out_count += 1
                if server.out_count == 3:
                    game_framework.change_mode(defence_mode)

    @staticmethod
    def do(ball):
        pass

    @staticmethod
    def draw(ball):
        sx, sy = ball.pos[0] - server.background.window_left, ball.pos[1] - server.background.window_bottom
        ball.image.clip_draw(ball.frame * 50, 0, 50, 50, sx, sy, 20, 20)


## 상태 머신 ##
class StateMachine:
    def __init__(self, ball):
        self.ball = ball
        self.cur_state = Idle
        self.transitions = {
            Idle: {throw_start: Throw, back_to_mound: Throw, throw_to_base: Throw, defender_catch: Idle},
            Throw: {throw_done: Idle, hit_success: Throw, defender_catch: Idle}
        }

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.ball, e)
                self.cur_state = next_state
                self.cur_state.enter(self.ball, e)
                return True
        return False

    def start(self):
        self.cur_state.enter(self.ball, ('START', 0))

    def update(self):
        self.cur_state.do(self.ball)

    def draw(self):
        self.cur_state.draw(self.ball)


class Ball:
    image = None

    def __init__(self):
        # 위치, 현재 프레임, 프레임의 길이
        self.pos = mound
        self.frame, self.frame_number = 0, 1
        # 목표 위치
        self.goal_position = home

        # 이미지 로드
        if Ball.image is None:
            Ball.image = load_image('resource/image/ball.png')

        # 타자의 달리기 속도
        self.RUN_SPEED_KMPH = random.randint(10, 14) / 10

        # 상태 머신 추가
        self.state_machine = StateMachine(self)
        self.state_machine.start()

        # 충돌 enter 시에만 충돌 하기 위해서 정의
        self.is_collision = False

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        sx, sy = self.pos[0] - server.background.window_left, self.pos[1] - server.background.window_bottom
        return sx - 10, sy - 10, sx + 10, sy + 10

    def handle_collision(self, group, other):
        if self.is_collision is False:
            # if other.state_machine.cur_state == hitter.HitterIdle:
            #     self.state_machine.handle_event(('DEFENDER_CATCH', 0))
            # else:
            #     self.state_machine.handle_event(('THROW_TO_BASE', other))
            self.is_collision = True
