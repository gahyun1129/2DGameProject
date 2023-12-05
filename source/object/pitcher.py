from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_SPACE

import game_framework
import server


# ## 이벤트 체크 함수 ##
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def throw_done(e):
    return e[0] == 'THROW_DONE'


def play_now(e):
    return e[0] == 'PLAY_NOW'


class Idle:
    @staticmethod
    def enter(pitcher, e):
        pitcher.frame, pitcher.frame_number, pitcher.action = 0, 5, 12

    @staticmethod
    def exit(pitcher, e):
        pass

    @staticmethod
    def do(pitcher):
        pitcher.frame = int(
            (pitcher.frame + pitcher.frame_number * pitcher.ACTION_PER_TIME * game_framework.frame_time)
            % pitcher.frame_number)

    @staticmethod
    def draw(pitcher):
        sx, sy = pitcher.pos[0] - server.background.window_left, pitcher.pos[1] - server.background.window_bottom
        pitcher.image.clip_draw(pitcher.frame * 100, (pitcher.action + pitcher.team_color) * 100, 100, 100, sx, sy)


class Throw:
    @staticmethod
    def enter(pitcher, e):
        pitcher.frame, pitcher.frame_number, pitcher.action = 0, 10, 11
        server.progress_bar.is_hit = True
        server.ui_ment.is_draw = False
        server.ui_ment.is_draw_number = False
        server.ui_judge.is_draw = False
        server.ui_judge.is_draw_number = False
        if e[0] == 'PLAY_NOW' and e[1] == 'ball':
            server.pitcher_ball = -0.3
        if e[0] == 'PLAY_NOW' and e[1] == 'strike':
            server.pitcher_ball = -0.5

    @staticmethod
    def exit(pitcher, e):
        # 공 생성, 이거 나중에 프레임 레이트에 맞춰서 시작하는 시간 다시 정해줘야 할 듯
        server.ball.state_machine.handle_event(('THROW_START', 0))
        server.ball.is_collision = False

        # 공이 날아오면서 타자는 공을 치는 애니메이션 시작!
        server.cur_hitter.state_machine.handle_event(('HIT_START', 0))

    @staticmethod
    def do(pitcher):
        pitcher.frame = int(
            (pitcher.frame + pitcher.frame_number * pitcher.ACTION_PER_TIME * game_framework.frame_time)
                % pitcher.frame_number)
        print(pitcher.frame, pitcher.frame_number, pitcher.ACTION_PER_TIME, game_framework.frame_time)
        if pitcher.frame == 0:
            pitcher.state_machine.handle_event(('THROW_DONE', 0))

    @staticmethod
    def draw(pitcher):
        sx, sy = pitcher.pos[0] - server.background.window_left, pitcher.pos[1] - server.background.window_bottom
        pitcher.image.clip_draw(pitcher.frame * 100, (pitcher.action + pitcher.team_color) * 100, 100, 100, sx,
                                sy)


## 상태 머신 ##
class StateMachineThrow:
    def __init__(self, pitcher):
        self.pitcher = pitcher
        self.cur_state = Idle
        self.transitions = {
            Idle: {space_down: Throw, play_now: Throw},
            Throw: {throw_done: Idle},
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

        # 파일: 이름, 탈삼진, 볼넷, ERA
        self.name, self.strike_out, self.four_balls, self.ERA = name, strike_out, four_balls, ERA

        # 이미지 로드
        if Pitcher.image is None:
            Pitcher.image = load_image('resource/image/animation.png')

        self.TIME_PER_ACTION = 1.0
        self.ACTION_PER_TIME = 1.0 / self.TIME_PER_ACTION

        # 상태 머신 추가
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

    def build_behavior_tree(self):
        pass

    def set_team_color(self, color):
        if color == '파랑':
            self.team_color = 13
        elif color == '빨강':
            self.team_color = 0
