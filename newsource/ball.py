import attack_mode
import game_world
import make_team
from define import *
from pico2d import load_image, draw_rectangle, get_time
import random


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
        # 투수가 공을 던지는 경우
        if e[0] == 'THROW_START':
            my_ball.pos = mound
            my_ball.goal_position = home
            # 공이 날아오면서 타자는 공을 치는 애니메이션 시작!
            attack_mode.cur_hitter.state_machine.handle_event(('HIT_START', 0))
        # 타자가 공을 친 경우
        elif e[0] == 'HIT_SUCCESS':
            my_ball.pos = home
            x = random.randint(50, 750)
            y = random.randint(300, 500)
            my_ball.goal_position = (x, y)
        # 공이 다시 마운드, 투수에게로 돌아가는 상황
        elif e[0] == 'BACK_TO_MOUND':
            my_ball.goal_position = mound
        # 가장 가까운 주자가 있는 base로 공을 던지는 경우 (수비)
        elif e[0] == 'THROW_TO_BASE':
            print(' 가까운 베이스로 던지기')
            pass
        my_ball.current_position = my_ball.pos
        my_ball.t = 0.0

    @staticmethod
    def exit(my_ball, e):
        # 마지막 위치 확실히 하기
        if e[0] != 'DEFENDER_CATCH':
            my_ball.pos = my_ball.goal_position
        pass

    @staticmethod
    def do(my_ball):
        my_ball.frame = (my_ball.frame + 1) % my_ball.frame_number
        x = (1 - my_ball.t) * my_ball.current_position[0] + my_ball.t * my_ball.goal_position[0]
        y = (1 - my_ball.t) * my_ball.current_position[1] + my_ball.t * my_ball.goal_position[1]
        my_ball.pos = (x, y)
        my_ball.t += 0.1

        # 목표 위치에 도착한 경우!!
        if my_ball.t > 1:
            my_ball.state_machine.handle_event(('THROW_DONE', 0))

    @staticmethod
    def draw(my_ball):
        my_ball.image.clip_draw(my_ball.frame * 50, 0, 50, 50, my_ball.pos[0], my_ball.pos[1], 20, 20)


class Idle:
    @staticmethod
    def enter(my_ball, e):
        if e[0] == 'DEFENDER_CATCH':
            my_ball.is_collision = True
            hitter = attack_mode.cur_hitter
            hitter.strike, hitter.ball = 0, 0
            make_team.set_next_hitter(hitter)
            game_world.remove_object(hitter)
            print('한 번에 잡음')

    @staticmethod
    def exit(my_ball, e):
        pass

    @staticmethod
    def do(my_ball):
        pass
        # if get_time() - my_ball.wait_time > 2:
        #     my_ball.state_machine.handle_event(('BACK_TO_MOUND', 0))

    @staticmethod
    def draw(my_ball):
        my_ball.image.clip_draw(my_ball.frame * 50, 0, 50, 50, my_ball.pos[0], my_ball.pos[1], 20, 20)


## 상태 머신 ##
class StateMachine:
    def __init__(self, my_ball):
        self.my_ball = my_ball
        self.cur_state = Idle
        self.transitions = {
            Idle: {throw_start: Throw, back_to_mound: Throw, throw_to_base: Throw},
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
        self.goal_position = home
        # 이미지 로드
        if Ball.image is None:
            Ball.image = load_image('resource/image/ball.png')

        # 상태머신 추가
        self.state_machine = StateMachine(self)
        self.state_machine.start()

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
            print('collision', self.state_machine.cur_state, other.name)
            if self.state_machine.cur_state == Throw:
                self.state_machine.handle_event(('DEFENDER_CATCH', 0))
            else:
                self.state_machine.handle_event(('THROW_TO_BASE', 0))
            self.is_collision = True
