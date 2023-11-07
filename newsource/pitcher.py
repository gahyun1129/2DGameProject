from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE

import attack_mode
import game_world
from ball import Ball


# ## 이벤트 체크 함수 ##
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def throw_done(e):
    return e[0] == 'THROW_DONE'


class Idle:
    @staticmethod
    def enter(pitcher, e):
        # action 값은 파란, 빨간 팀 모두 같음
        # 나중에 draw 할 때 team_color 값을 더해서 색 구분 하자!
        pitcher.frame, pitcher.frame_number, pitcher.action = 0, 1, 0

    @staticmethod
    def exit(pitcher, e):
        pass

    @staticmethod
    def do(pitcher):
        pitcher.frame = (pitcher.frame + 1) % pitcher.frame_number
        # print('Idle Do')

    @staticmethod
    def draw(pitcher):
        pitcher.image.clip_draw(pitcher.frame * 50, (pitcher.action + pitcher.team_color) * 50, 50, 50, pitcher.pos[0],
                                pitcher.pos[1])


class Throw:
    @staticmethod
    def enter(pitcher, e):
        # action 값은 파란, 빨간 팀 모두 같음
        # 나중에 draw 할 때 team_color 값을 더해서 색 구분 하자!
        pitcher.frame, pitcher.frame_number, pitcher.action = 0, 1, 1

        pitcher.wait_time = get_time()

    @staticmethod
    def exit(pitcher, e):
        pass

    @staticmethod
    def do(pitcher):
        pitcher.frame = (pitcher.frame + 1) % pitcher.frame_number
        if get_time() - pitcher.wait_time > 2:
            pitcher.state_machine.handle_event(('THROW_DONE', 0))

    @staticmethod
    def draw(pitcher):
        pitcher.image.clip_draw(pitcher.frame * 50, (pitcher.action + pitcher.team_color) * 50, 50, 50, pitcher.pos[0],
                                pitcher.pos[1])


## 상태 머신 ##
class StateMachineThrow:
    def __init__(self, pitcher):
        self.pitcher = pitcher
        self.cur_state = Idle
        self.transitions = {
            Throw: {throw_done: Idle},
            Idle: {space_down: Throw},
        }

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.pitcher, e)
                self.cur_state = next_state
                self.cur_state.enter(self.pitcher, e)
                return True
        return False

    def start(self):
        self.cur_state.enter(self.pitcher, ('START', 0))

    def update(self):
        self.cur_state.do(self.pitcher)

    def draw(self):
        self.cur_state.draw(self.pitcher)


## 클래스 ##
class Pitcher:
    image = None

    def __init__(self, pos, name, strike_out, four_balls, ERA, pitching):
        # 위치, 현재 프레임, 현재 action, 프레임의 길이
        self.pos = pos
        self.frame, self.frame_number, self.action = 0, 1, 0
        self.team_color = 0

        # 파일: 이름, 탈삼진, 볼넷, ERA, 투구법 2개
        self.name, self.strike_out, self.four_balls, self.ERA, self.pitching = name, strike_out, four_balls, ERA, pitching

        # 이미지 로드
        if Pitcher.image is None:
            Pitcher.image = load_image('resource/image/character_hitter.png')

        # # 상태머신 추가
        self.state_machine = None

    def init_state_machine(self, type):
        if type == '수비수':
            self.state_machine = StateMachineThrow(self)
        self.state_machine.start()
        pass

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
