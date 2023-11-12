import define
import game_framework
import mode_attack
import game_world
import game_make_team
import mode_defence
import player_hitter_statemachine
from define import *
from pico2d import load_image, draw_rectangle, get_time
import random

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
    def enter(my_ball, e):
        my_ball.frame, my_ball.frame_number = 0, 1
        my_ball.event = e[0]
        # 투수가 공을 던지는 경우
        if e[0] == 'THROW_START':
            my_ball.pos = mound
            my_ball.goal_position = home
        # 타자가 공을 친 경우
        elif e[0] == 'HIT_SUCCESS':
            my_ball.pos = home
            x = random.randint(50, 750)
            y = random.randint(300, 500)
            my_ball.goal_position = (x, y)
        # 공이 다시 마운드, 투수에게로 돌아가는 상황
        elif e[0] == 'BACK_TO_MOUND':
            my_ball.goal_position = mound
        # 가장 가까운 주자가 있는 base 공을 던지는 경우 (수비)
        elif e[0] == 'THROW_TO_BASE':
            my_ball.goal_position = e[1].throw_to_base()
            print('e[1].throw_to_base(), 가까운 베이스로 던지기')
            pass
        my_ball.current_position = my_ball.pos
        my_ball.t = 0.0

    @staticmethod
    def exit(my_ball, e):
        # if my_ball.event == 'BACK_TO_MOUND':
        #     hitter = mode_attack.cur_hitter
        #     game_make_team.set_next_hitter(hitter)
        if my_ball.event == 'THROW_TO_BASE':
            if define.number_to_bases[my_ball.goal_position].hasDefender and not define.number_to_bases[my_ball.goal_position].hasRunner:
                print('ball done')
                hitter = mode_attack.cur_hitter
                hitter.strike, hitter.my_ball = 0, 0
                game_make_team.set_next_hitter(hitter)
                game_world.remove_object(hitter)
                mode_attack.out_count += 1
                if mode_attack.out_count == 3:
                    game_framework.change_mode(mode_defence)
        pass

    @staticmethod
    def do(my_ball):
        my_ball.frame = (my_ball.frame + 1) % my_ball.frame_number
        x = (1 - my_ball.t) * my_ball.current_position[0] + my_ball.t * my_ball.goal_position[0]
        y = (1 - my_ball.t) * my_ball.current_position[1] + my_ball.t * my_ball.goal_position[1]
        my_ball.pos = (x, y)
        # my_ball.t += 0.1 * ((my_ball.RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * PIXEL_PER_METER * game_framework.frame_time
        my_ball.t += 1
        # 목표 위치에 도착한 경우!!
        if my_ball.t > 1:
            # 마지막 위치 확실히 하기
            my_ball.pos = my_ball.goal_position
            my_ball.state_machine.handle_event(('THROW_DONE', 0))

    @staticmethod
    def draw(my_ball):
        my_ball.image.clip_draw(my_ball.frame * 50, 0, 50, 50, my_ball.pos[0], my_ball.pos[1], 20, 20)


class Idle:
    @staticmethod
    def enter(my_ball, e):
        if e[0] == 'DEFENDER_CATCH':
            # 타자 삭제
            hitter = mode_attack.cur_hitter
            hitter.strike, hitter.my_ball = 0, 0
            game_make_team.set_next_hitter(hitter)
            game_world.remove_object(hitter)
            my_ball.state_machine.handle_event(('BACK_TO_MOUND', 0))
            for player in game_world.defence_team[1:9]:
                player.state_machine.handle_event(('RUN_DONE', 0))
            # 수비수가 공 잡으려고 달리는 것도 멈춰야 함.
            print('한 번에 잡음')
        if my_ball.pos != mound and my_ball.is_collision:
            my_ball.state_machine.handle_event(('BACK_TO_MOUND', 0))

    @staticmethod
    def exit(my_ball, e):
        pass

    @staticmethod
    def do(my_ball):
        pass

    @staticmethod
    def draw(my_ball):
        my_ball.image.clip_draw(my_ball.frame * 50, 0, 50, 50, my_ball.pos[0], my_ball.pos[1], 20, 20)


## 상태 머신 ##
class StateMachine:
    def __init__(self, my_ball):
        self.my_ball = my_ball
        self.cur_state = Idle
        self.transitions = {
            Idle: {throw_start: Throw, back_to_mound: Throw, throw_to_base: Throw, defender_catch: Idle},
            Throw: {throw_done: Idle, hit_success: Throw, defender_catch: Idle}
        }

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.my_ball, e)
                self.cur_state = next_state
                self.cur_state.enter(self.my_ball, e)
                return True
        return False

    def start(self):
        self.cur_state.enter(self.my_ball, ('START', 0))

    def update(self):
        self.cur_state.do(self.my_ball)

    def draw(self):
        self.cur_state.draw(self.my_ball)


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
        return self.pos[0] - 10, self.pos[1] - 10, self.pos[0] + 10, self.pos[1] + 10

    def handle_collision(self, group, other):
        if self.is_collision is False:
            print('collision', other.state_machine.cur_state, other.name)
            print('collision', self.state_machine.cur_state)
            if other.state_machine.cur_state == player_hitter_statemachine.Idle:
                self.state_machine.handle_event(('DEFENDER_CATCH', 0))
            else:
                self.state_machine.handle_event(('THROW_TO_BASE', other))
            self.is_collision = True