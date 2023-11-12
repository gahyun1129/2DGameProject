from pico2d import load_image, load_font, draw_rectangle

import game_world
import mode_attack

from define import *

import random

from player_hitter_statemachine import StateMachineRun, StateMachineHit, StateMachineDefence

PIXEL_PER_METER = (10.0 / 0.3)

state_machines = {
    '주자': StateMachineRun,
    '타자': StateMachineHit,
    '수비수': StateMachineDefence
}


## 클래스 ##
class Hitter:
    image = None

    def __init__(self, pos, name, hit, home_run, BA, OPS):
        # 위치, 현재 프레임, 현재 action, 프레임의 길이
        self.pos = pos
        self.frame, self.frame_number, self.action = 0, 1, 4

        self.team_color = 0

        self.font = load_font('resource/txt/NanumGothic.TTF', 16)

        # 파일: 이름, 안타, 홈런, 타율, 출루율 + 장타율
        self.name, self.hit, self.home_run, self.BA, self.OPS = \
            name, hit, home_run, BA, OPS

        # 목표 위치, 수비 위치 (수비 시 사용)
        self.goal_position, self.defence_position = None, None

        # 타자의 스트라이크, 볼 개수 저장 변수
        self.strike, self.ball = 2, 3

        # 타자의 달리기 속도
        self.RUN_SPEED_KMPH = random.randint(4, 8) / 10

        # 수비수의 base 위치
        self.base = None

        # 이미지 로드
        if Hitter.image is None:
            Hitter.image = load_image('resource/image/character_hitter.png')

        # 상태 머신 추가
        self.state_machine = None

    def set_team_color(self, color):
        if color == '파랑':
            self.team_color = 1
        elif color == '빨강':
            self.team_color = 0

    def init_state_machine(self, type):
        # 객체를 따로 만들어 주었으므로, 상태 머신 시작을 다시 해야 함.
        self.state_machine = state_machines[type](self)
        self.state_machine.start()

        # 수비수의 수비 위치 저장해 두기
        self.defence_position = self.pos

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.pos[0] - 20, self.pos[1] - 30, self.pos[0] + 20, self.pos[1] + 30

    def handle_collision(self, group, other):
        pass

    def throw_to_base(self):
        for base in next_base[self.defence_position]:
            if positions[base][1]:
                return base
            return mode_attack.cur_hitter.goal_position

    def run_to_ball(self, goal_pos):
        # x: 400 이상, y: 350 이상 > 중견수, 우익수
        if goal_pos[0] >= 400 and self.pos[0] >= 400 and goal_pos[1] >= 350 and self.pos[1] >= 350: return True
        # x: 400 이하, y: 300 이상 > 좌익수, 중견수
        if goal_pos[0] <= 400 and self.pos[0] <= 400 and goal_pos[1] >= 350 and self.pos[1] >= 350: return True
        # x: 400 이상, y: 300 이하 > 1루수, 2루수
        if goal_pos[0] >= 400 and self.pos[0] >= 400 and goal_pos[1] >= 350 and self.pos[1] >= 350: return True
        # x: 400 이하, y: 300 이하 > 유격수, 3루수
        if goal_pos[0] <= 400 and self.pos[0] <= 400 and goal_pos[1] <= 350 and self.pos[1] <= 350: return True
        return False
