from pico2d import get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE
import game_framework
import mode_defence
import mode_attack
import player_hitter
import game_make_team
import game_world
import random

from define import *


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


def stay_here(e):
    return e[0] == 'STAY_HERE'


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
        hitter.image.clip_draw(hitter.frame * 100, (hitter.action + hitter.team_color) * 100, 100, 100, hitter.pos[0],
                               hitter.pos[1], 100*3, 100*3)


class Hit:
    @staticmethod
    def enter(hitter, e):
        # action 값은 파란, 빨간 팀 모두 같음
        # 나중에 draw 할 때 team_color 값을 더해서 색 구분 하자!
        hitter.frame, hitter.frame_number, hitter.action = 0, 1, 2
        hitter.wait_time = get_time()
        mode_attack.make_ui.is_update = False
        hitter.user_force = (mode_attack.make_ui.action * 10 + mode_attack.make_ui.frame) / 100
        print(hitter.user_force)
    @staticmethod
    def exit(hitter, e):
        pass

    @staticmethod
    def do(hitter):
        hitter.frame = (hitter.frame + 1) % hitter.frame_number
        if get_time() - hitter.wait_time > 0:
            # hit = hitter.user_force + float(hitter.BA) * random.randint(0, 3)
            # hit = 0.6 # 항상 볼
            # hit = 0.3  # 항상 스트라이크
            hit = 1.1  # 항상 hit
            if hit > 1:
                # print(attack_mode.ball.goal_position)
                hitter.strike, hitter.ball = 0, 0
                mode_attack.my_ball.state_machine.handle_event(('HIT_SUCCESS', 0))
                hitter.state_machine.handle_event(('HIT_SUCCESS', 0))
                game_world.update_handle_event(('HIT_SUCCESS', 0))
                print(mode_attack.my_ball.goal_position, hitter.name)
            else:
                hitter.wait_time = get_time()
                if hit < 0.4:
                    hitter.strike += 1
                else:
                    hitter.ball += 1
                if hitter.strike == 3:
                    print('STRIKE_3')
                    hitter.strike, hitter.ball = 0, 0
                    game_make_team.set_next_hitter(hitter)
                    game_world.remove_object(hitter)
                    mode_attack.out_count += 1
                    if mode_attack.out_count == 3:
                        game_framework.change_mode(mode_defence)
                elif hitter.ball == 4:
                    print('BALL_4')
                    hitter.strike, hitter.ball = 0, 0
                    hitter.state_machine.handle_event(('FOUR_BALL', 0))
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
            mode_attack.goal_runner = hitter

    @staticmethod
    def exit(hitter, e):
        # 위치를 확실히 하기 위해 한 번 더 정의
        hitter.pos = hitter.goal_position
        positions[hitter.pos][1] = True
        print('hitter done')

    @staticmethod
    def do(hitter):
        # 프레임 넘기기
        hitter.frame = (hitter.frame + 1) % hitter.frame_number

        # 직선 이동 방정식
        x = (1 - hitter.t) * hitter.current_position[0] + hitter.t * hitter.goal_position[0]
        y = (1 - hitter.t) * hitter.current_position[1] + hitter.t * hitter.goal_position[1]
        hitter.pos = (x, y)
        hitter.t += 0.1 * ((
                                       hitter.RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * player_hitter.PIXEL_PER_METER * game_framework.frame_time

        # 직선 이동이 끝날 때 run_success 이벤트 발생
        if hitter.t > 1:
            hitter.state_machine.handle_event(('RUN_DONE', 0))
            hitter.init_state_machine('주자')
            game_make_team.set_next_hitter(hitter)
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
        # home 에 도착한 경우,,,
        if hitter.pos == home:
            mode_attack.goal_runner = hitter
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
        hitter.t += 0.1 * ((
                                       hitter.RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * player_hitter.PIXEL_PER_METER * game_framework.frame_time

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
        hitter.goal_position = mode_attack.my_ball.goal_position
        hitter.t = 0.0

        # 만약 공이 수비수가 움직이지 않아도 되는 위치에 온다면,
        if hitter.goal_position[0] - 5 < hitter.pos[0] < hitter.goal_position[0] + 5 \
                and hitter.goal_position[1] - 5 < hitter.pos[1] < hitter.goal_position[1] + 5:
            hitter.state_machine.handle_event(('STAY_HERE', 0))

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
        hitter.t += 0.1 * ((
                                       hitter.RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * player_hitter.PIXEL_PER_METER * game_framework.frame_time

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
        hitter.goal_position = hitter.defence_position
        hitter.t = 0.0

    @staticmethod
    def exit(hitter, e):
        # 위치를 확실히 하기 위해 한 번 더 정의
        hitter.pos = hitter.defence_position

    @staticmethod
    def do(hitter):
        # 프레임 넘기기
        hitter.frame = (hitter.frame + 1) % hitter.frame_number

        # 직선 이동 방정식
        x = (1 - hitter.t) * hitter.current_position[0] + hitter.t * hitter.goal_position[0]
        y = (1 - hitter.t) * hitter.current_position[1] + hitter.t * hitter.goal_position[1]
        hitter.pos = (x, y)
        hitter.t += 0.1 * ((
                                       hitter.RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * player_hitter.PIXEL_PER_METER * game_framework.frame_time

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
        self.hitter.font.draw(self.hitter.pos[0] - 10, self.hitter.pos[1] + 50, f'{self.hitter.name}', (0, 255, 0))


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
        self.hitter.font.draw(self.hitter.pos[0] - 10, self.hitter.pos[1] + 50, f'{self.hitter.name}', (0, 0, 255))


class StateMachineDefence:
    def __init__(self, hitter):
        self.hitter = hitter

        self.cur_state = Idle
        self.transitions = {
            Idle: {hit_success: RunDefence},
            RunDefence: {run_done: RunPosition, stay_here: Idle},
            RunPosition: {run_done: Idle},
        }

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.hitter, e)
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
