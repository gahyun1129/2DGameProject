from pico2d import load_image, get_time, load_font
from sdl2 import SDL_KEYDOWN, SDLK_SPACE
from define import *
import random

import attack_mode
import make_team
import game_world


## 이벤트 체크 함수 ##
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):
    return e[0] == 'TIME_OUT'


def run_done(e):
    return e[0] == 'RUN_DONE'


def hit_fail(e):
    return e[0] == 'HIT_FAIL'


def hit_success(e):
    return e[0] == 'HIT_SUCCESS'


def hit_done(e):
    return e[0] == 'HIT_DONE'


def hit_start(e):
    return e[0] == 'HIT_START'


def four_ball(e):
    return e[0] == 'FOUR_BALL'


## 상태 ##
class Idle:
    @staticmethod
    def enter(hitter, e):
        # action 값은 파란, 빨간 팀 모두 같음
        # 나중에 draw 할 때 team_color 값을 더해서 색 구분 하자!
        hitter.frame, hitter.frame_number, hitter.action = 0, 1, 4

    @staticmethod
    def exit(hitter, e):
        pass

    @staticmethod
    def do(hitter):
        hitter.frame = (hitter.frame + 1) % hitter.frame_number
        # print('Idle Do')

    @staticmethod
    def draw(hitter):
        hitter.image.clip_draw(hitter.frame * 50, (hitter.action + hitter.team_color) * 50, 50, 50, hitter.pos[0],
                               hitter.pos[1])


class Hit:
    @staticmethod
    def enter(hitter, e):
        # action 값은 파란, 빨간 팀 모두 같음
        # 나중에 draw 할 때 team_color 값을 더해서 색 구분 하자!
        hitter.frame, hitter.frame_number, hitter.action = 0, 1, 2

        hitter.wait_time = get_time()

    @staticmethod
    def exit(hitter, e):
        pass

    @staticmethod
    def do(hitter):
        hitter.frame = (hitter.frame + 1) % hitter.frame_number
        if get_time() - hitter.wait_time > 0:
            # hit = 0.3 + float(hitter.BA) * random.randint(0, 3)
            # hit = 0.6 # 항상 볼
            hit = 0.3 # 항상 스트라이크
            # hit = 1.1 # 항상 hit
            if hit > 1:
                print(attack_mode.ball.goal_position)
                hitter.strike, hitter.ball = 0, 0
                attack_mode.ball.state_machine.handle_event(('HIT_SUCCESS', 0))
                hitter.state_machine.handle_event(('HIT_SUCCESS', 0))
                game_world.update_handle_event(('HIT_SUCCESS', 0))
                print(attack_mode.ball.goal_position)
            else:
                hitter.wait_time = get_time()
                if hit < 0.4:
                    hitter.strike += 1
                else:
                    hitter.ball += 1
                if hitter.strike == 3:
                    print('STRIKE_3')
                    hitter.strike, hitter.ball = 0, 0
                    make_team.set_next_hitter(hitter)
                    game_world.remove_object(hitter)
                elif hitter.ball == 4:
                    print('BALL_4')
                    hitter.strike, hitter.ball = 0, 0
                    hitter.state_machine.handle_event(('FOUR_BALL', 0))
                    attack_mode.ball.delete_self()
                    game_world.update_handle_event(('FOUR_BALL', 0))
                else:
                    hitter.state_machine.handle_event(('HIT_FAIL', 0))

        # print('Hit Do')

    @staticmethod
    def draw(hitter):
        hitter.image.clip_draw(hitter.frame * 50, (hitter.action + hitter.team_color) * 50, 50, 50, hitter.pos[0],
                               hitter.pos[1])


class HitAndRun:
    @staticmethod
    def enter(hitter, e):
        # action 값은 파란, 빨간 팀 모두 같음
        # 나중에 draw 할 때 team_color 값을 더해서 색 구분 하자!
        hitter.frame, hitter.frame_number, hitter.action = 0, 1, 0

        # 현재 위치, 목표 위치, 매개 변수 t 정의
        hitter.current_position = hitter.pos
        hitter.goal_position = positions[hitter.pos][0]
        hitter.t = 0.0

        # home에 도착한 경우,,,
        if hitter.goal_position == home:
            attack_mode.goal_runner = hitter

    @staticmethod
    def exit(hitter, e):
        # 위치를 확실히 하기 위해 한 번 더 정의
        hitter.pos = hitter.goal_position
        positions[hitter.pos][1] = True

    @staticmethod
    def do(hitter):
        # 프레임 넘기기
        hitter.frame = (hitter.frame + 1) % hitter.frame_number

        # 직선 이동 방정식
        x = (1 - hitter.t) * hitter.current_position[0] + hitter.t * hitter.goal_position[0]
        y = (1 - hitter.t) * hitter.current_position[1] + hitter.t * hitter.goal_position[1]
        hitter.pos = (x, y)
        hitter.t += 0.1

        # 직선 이동이 끝날 때 run_success 이벤트 발생
        if hitter.t > 1:
            hitter.state_machine.handle_event(('RUN_DONE', 0))
            hitter.init_state_machine('주자')
            make_team.set_next_hitter(hitter)
        # print('Run Do')

    @staticmethod
    def draw(hitter):
        hitter.image.clip_draw(hitter.frame * 50, (hitter.action + hitter.team_color) * 50, 50, 50, hitter.pos[0],
                               hitter.pos[1])


class Run:
    @staticmethod
    def enter(hitter, e):
        # action 값은 파란, 빨간 팀 모두 같음
        # 나중에 draw 할 때 team_color 값을 더해서 색 구분 하자!
        hitter.frame, hitter.frame_number, hitter.action = 0, 1, 0

        # 현재 위치, 목표 위치, 매개 변수 t 정의
        hitter.current_position = hitter.pos
        hitter.goal_position = positions[hitter.pos][0]
        hitter.t = 0.0

        if positions[positions[hitter.pos][2]][1] is False:
            hitter.state_machine.handle_event(('RUN_DONE', 0))


    @staticmethod
    def exit(hitter, e):
        # 위치를 확실히 하기 위해 한 번 더 정의
        hitter.pos = hitter.goal_position
        # home에 도착한 경우,,,
        if hitter.pos == home:
            attack_mode.goal_runner = hitter
            game_world.remove_object(hitter)
        positions[hitter.pos][1] = True

    @staticmethod
    def do(hitter):
        # 프레임 넘기기
        hitter.frame = (hitter.frame + 1) % hitter.frame_number

        # 직선 이동 방정식
        x = (1 - hitter.t) * hitter.current_position[0] + hitter.t * hitter.goal_position[0]
        y = (1 - hitter.t) * hitter.current_position[1] + hitter.t * hitter.goal_position[1]
        hitter.pos = (x, y)
        hitter.t += 0.1

        # 직선 이동이 끝날 때 run_success 이벤트 발생
        if hitter.t > 1:
            hitter.state_machine.handle_event(('RUN_DONE', 0))

    @staticmethod
    def draw(hitter):
        hitter.image.clip_draw(hitter.frame * 50, (hitter.action + hitter.team_color) * 50, 50, 50, hitter.pos[0],
                               hitter.pos[1])


class RunDefence:
    @staticmethod
    def enter(hitter, e):
        # action 값은 파란, 빨간 팀 모두 같음
        # 나중에 draw 할 때 team_color 값을 더해서 색 구분 하자!
        hitter.frame, hitter.frame_number, hitter.action = 0, 1, 0

        # 현재 위치, 목표 위치, 매개 변수 t 정의
        hitter.current_position = hitter.pos
        hitter.goal_position = attack_mode.ball.goal_position
        hitter.t = 0.0

    @staticmethod
    def exit(hitter, e):
        # 위치를 확실히 하기 위해 한 번 더 정의
        hitter.pos = hitter.goal_position

    @staticmethod
    def do(hitter):
        # 프레임 넘기기
        hitter.frame = (hitter.frame + 1) % hitter.frame_number

        # 직선 이동 방정식
        x = (1 - hitter.t) * hitter.current_position[0] + hitter.t * hitter.goal_position[0]
        y = (1 - hitter.t) * hitter.current_position[1] + hitter.t * hitter.goal_position[1]
        hitter.pos = (x, y)
        hitter.t += 0.1

        # 직선 이동이 끝날 때 RUN_DONE 이벤트 발생
        if hitter.t > 1:
            hitter.state_machine.handle_event(('RUN_DONE', 0))
        # print('Run Do')

    @staticmethod
    def draw(hitter):
        hitter.image.clip_draw(hitter.frame * 50, (hitter.action + hitter.team_color) * 50, 50, 50, hitter.pos[0],
                               hitter.pos[1])


class RunPosition:
    @staticmethod
    def enter(hitter, e):
        # action 값은 파란, 빨간 팀 모두 같음
        # 나중에 draw 할 때 team_color 값을 더해서 색 구분 하자!
        hitter.frame, hitter.frame_number, hitter.action = 0, 1, 0

        # 현재 위치, 목표 위치, 매개 변수 t 정의
        hitter.current_position = hitter.pos
        hitter.goal_position = hitter.defence_pos
        hitter.t = 0.0

    @staticmethod
    def exit(hitter, e):
        # 위치를 확실히 하기 위해 한 번 더 정의
        hitter.pos = hitter.defence_pos

    @staticmethod
    def do(hitter):
        # 프레임 넘기기
        hitter.frame = (hitter.frame + 1) % hitter.frame_number

        # 직선 이동 방정식
        x = (1 - hitter.t) * hitter.current_position[0] + hitter.t * hitter.goal_position[0]
        y = (1 - hitter.t) * hitter.current_position[1] + hitter.t * hitter.goal_position[1]
        hitter.pos = (x, y)
        hitter.t += 0.1

        # 직선 이동이 끝날 때 RUN_DONE 이벤트 발생
        if hitter.t > 1:
            hitter.state_machine.handle_event(('RUN_DONE', 0))
        # print('Run Do')

    @staticmethod
    def draw(hitter):
        hitter.image.clip_draw(hitter.frame * 50, (hitter.action + hitter.team_color) * 50, 50, 50, hitter.pos[0],
                               hitter.pos[1])


## 상태 머신 ##
class StateMachineHit:
    def __init__(self, hitter):
        self.hitter = hitter
        self.cur_state = Idle
        self.transitions = {
            Idle: {hit_start: Hit},
            Hit: {hit_success: HitAndRun, hit_fail: Idle, four_ball: HitAndRun},
            HitAndRun: {run_done: Idle}
        }

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.hitter, e)
                attack_mode.current_event = e
                self.cur_state = next_state
                self.cur_state.enter(self.hitter, e)
                return True
        return False

    def start(self):
        self.cur_state.enter(self.hitter, ('START', 0))

    def update(self):
        self.cur_state.do(self.hitter)

    def draw(self):
        self.cur_state.draw(self.hitter)
        self.hitter.font.draw(self.hitter.pos[0] - 10, self.hitter.pos[1] + 50, f'{self.hitter.name}', (255, 255, 0))


class StateMachineRun:
    def __init__(self, hitter):
        self.hitter = hitter
        self.cur_state = Idle
        self.transitions = {
            Idle: {hit_success: Run, four_ball: Run},
            Run: {run_done: Idle}
        }

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.hitter, e)
                attack_mode.current_event = e
                self.cur_state = next_state
                self.cur_state.enter(self.hitter, e)
                return True
        return False

    def start(self):
        self.cur_state.enter(self.hitter, ('START', 0))

    def update(self):
        self.cur_state.do(self.hitter)

    def draw(self):
        self.cur_state.draw(self.hitter)
        self.hitter.font.draw(self.hitter.pos[0] - 10, self.hitter.pos[1] + 50, f'{self.hitter.name}', (255, 255, 0))


class StateMachineDefence:
    def __init__(self, hitter):
        self.hitter = hitter
        self.cur_state = Idle
        self.transitions = {
            Idle: {hit_success: RunDefence},
            RunDefence: {run_done: RunPosition},
            RunPosition: {run_done: Idle},
        }

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.hitter, e)
                attack_mode.current_event = e
                self.cur_state = next_state
                self.cur_state.enter(self.hitter, e)
                return True
        return False

    def start(self):
        self.cur_state.enter(self.hitter, ('START', 0))

    def update(self):
        self.cur_state.do(self.hitter)

    def draw(self):
        self.cur_state.draw(self.hitter)


## 클래스 ##
class Hitter:
    image = None

    def __init__(self, pos, name, hit, home_run, stolen_base, BA, OPS):
        # 위치, 현재 프레임, 현재 action, 프레임의 길이
        self.pos = pos
        self.frame, self.frame_number, self.action = 0, 1, 4
        self.team_color = 0
        self.font = load_font('resource/txt/NanumGothic.TTF', 16)
        # 파일: 이름, 안타, 홈런, 도루, 타율, 출루율 + 장타율
        self.name, self.hit, self.home_run, self.stolen_base, self.BA, self.OPS = name, hit, home_run, stolen_base, BA, OPS

        # 타자의 스트라이크, 볼 개수 저장 변수
        self.strike, self.ball = 2, 3

        # 이미지 로드
        if Hitter.image is None:
            Hitter.image = load_image('resource/image/character_hitter.png')

        # # 상태머신 추가
        self.state_machine = None
        # self.state_machine.start()

    def set_team_color(self, color):
        if color == '파랑':
            self.team_color = 1
        elif color == '빨강':
            self.team_color = 0

    def init_state_machine(self, type):
        # 객체를 따로 만들어 주었으므로, 상태 머신 시작을 다시 해야 함.
        if type == '수비수':
            self.state_machine = StateMachineDefence(self)
        elif type == '타자':
            self.state_machine = StateMachineHit(self)
        elif type == '주자':
            self.state_machine = StateMachineRun(self)
        self.state_machine.start()
        # 수비수의 수비 위치
        self.defence_pos = self.pos

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def update(self):
        self.state_machine.update()
        # self.frame = (self.frame + 1) % self.frame_number

    def draw(self):
        self.state_machine.draw()
        # Hitter.image.clip_draw(self.frame * 50, self.action * 50, 50, 50, self.x, self.y)

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
