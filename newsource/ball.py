import attack_mode
import game_world
from define import *
from pico2d import load_image, draw_rectangle
import random


def throw_start(e):
    return e[0] == 'THROW_START'


def throw_done(e):
    return e[0] == 'THROW_DONE'


def hit_success(e):
    return e[0] == 'HIT_SUCCESS'


def defence_done(e):
    return e[0] == 'DEFENCE_DONE'


def fly_done(e):
    return e[0] == 'FLY_DONE'


class Throw:
    @staticmethod
    def enter(ballObj, e):
        ballObj.isDraw = True

        ballObj.frame, ballObj.frame_number =0, 1
        ballObj.current_position = ballObj.pos
        ballObj.goal_position = home
        ballObj.t = 0.0

        # 공이 날아오면서 타자는 공을 치는 애니메이션 시작!
        attack_mode.cur_hitter.state_machine.handle_event(('HIT_START', 0))

    @staticmethod
    def exit(ballObj, e):
        pass

    @staticmethod
    def do(ballObj):
        ballObj.frame = (ballObj.frame + 1) % ballObj.frame_number
        x = (1 - ballObj.t) * ballObj.current_position[0] + ballObj.t * ballObj.goal_position[0]
        y = (1 - ballObj.t) * ballObj.current_position[1] + ballObj.t * ballObj.goal_position[1]
        ballObj.pos = (x, y)
        ballObj.t += 0.5

        if ballObj.t > 1:
            ballObj.state_machine.handle_event(('THROW_DONE', 0))

    @staticmethod
    def draw(ballObj):
        ballObj.image.clip_draw(ballObj.frame * 50, 0, 50, 50, ballObj.pos[0], ballObj.pos[1], 20, 20)


class Idle:
    @staticmethod
    def enter(ballObj, e):
        pass

    @staticmethod
    def exit(ballObj, e):
        ballObj.pos = mound

    @staticmethod
    def do(ballObj):
        pass

    @staticmethod
    def draw(ballObj):
        ballObj.image.clip_draw(ballObj.frame * 50, 0, 50, 50, ballObj.pos[0], ballObj.pos[1], 20, 20)


class Fly:
    @staticmethod
    def enter(ballObj, e):
        ballObj.isDraw = True
        ballObj.pos, ballObj.frame, ballObj.frame_number = home, 0, 1
        ballObj.current_position = ballObj.pos
        x = random.randint(50, 750)
        y = random.randint(300, 500)
        ballObj.goal_position = (x, y)
        ballObj.t = 0.0

    @staticmethod
    def exit(pitcher, e):
        pass

    @staticmethod
    def do(ballObj):
        ballObj.frame = (ballObj.frame + 1) % ballObj.frame_number
        x = (1 - ballObj.t) * ballObj.current_position[0] + ballObj.t * ballObj.goal_position[0]
        y = (1 - ballObj.t) * ballObj.current_position[1] + ballObj.t * ballObj.goal_position[1]
        ballObj.pos = (x, y)
        ballObj.t += 0.1

        if ballObj.t > 1:
            ballObj.state_machine.handle_event(('FLY_DONE', 0))

    @staticmethod
    def draw(ballObj):
        ballObj.image.clip_draw(ballObj.frame * 50, 0, 50, 50, ballObj.pos[0], ballObj.pos[1], 20, 20)


## 상태 머신 ##
class StateMachine:
    def __init__(self, ballObj):
        self.ballObj = ballObj
        self.cur_state = Idle
        self.transitions = {
            Idle: {throw_start: Throw, hit_success: Fly},
            Throw: {throw_done: Idle, hit_success: Fly},
            Fly: {defence_done: Idle, fly_done: Idle, throw_start:Throw}
        }

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.ballObj, e)
                self.cur_state = next_state
                self.cur_state.enter(self.ballObj, e)
                return True
        return False

    def start(self):
        self.cur_state.enter(self.ballObj, ('START', 0))

    def update(self):
        self.cur_state.do(self.ballObj)

    def draw(self):
        self.cur_state.draw(self.ballObj)


class Ball:
    image = None

    def __init__(self):
        # 위치, 현재 프레임, 프레임의 길이
        self.pos = mound
        self.frame, self.frame_number = 0, 1
        self.isDraw = False
        self.goal_position = home
        # 이미지 로드
        if Ball.image is None:
            Ball.image = load_image('resource/image/ball.png')

        # 상태머신 추가
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        if self.isDraw:
            self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        if self.isDraw:
            self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.pos[0] - 10, self.pos[1] - 10, self.pos[0] + 10, self.pos[1] + 10

    def handle_collision(self, group, other):
        print('collision')
        self.state_machine.handle_event(('THROW', 0))
