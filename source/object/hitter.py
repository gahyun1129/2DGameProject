from pico2d import load_image, load_font, draw_rectangle

import game_framework
import server
import random

import mode.defence_mode as defence_mode
import module.make_team as make_team
import object.ball as obj_ball
from object.base import *

PIXEL_PER_METER = (10.0 / 0.3)


## 이벤트 체크 함수 ##
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


def super_catch(e):
    return e[0] == 'SUPER_CATCH'


def throw_to_near_base(e):
    return e[0] == 'THROW_TO_NEAR_BASE'


def back_to_defence(e):
    return e[0] == 'BACK_TO_DEFENCE'


def draw_hitter(hitter):
    sx, sy = hitter.pos[0] - server.background.window_left, hitter.pos[1] - server.background.window_bottom
    hitter.image.clip_draw(hitter.frame * 100, (hitter.action + hitter.team_color) * 100, 100, 100, sx, sy)


def set_next_hitter(hitter):
    hitter.strike, hitter.ball = 0, 0
    make_team.search_next_hitter(hitter)
    game_world.remove_object(hitter)
    server.out_count += 1
    if server.out_count == 3:
        pass
        # game_framework.change_mode(defence_mode)


## 상태 ##
class HitterIdle:
    @staticmethod
    def enter(hitter, e):
        hitter.frame, hitter.frame_number, hitter.action = 0, 6, 10
        # hitter.frame, hitter.frame_number, hitter.action = 0, 7, 4

    @staticmethod
    def exit(hitter, e):
        pass

    @staticmethod
    def do(hitter):
        hitter.frame = (hitter.frame + 1) % hitter.frame_number

    @staticmethod
    def draw(hitter):
        draw_hitter(hitter)


class RunnerIdle:
    @staticmethod
    def enter(hitter, e):
        hitter.frame, hitter.frame_number, hitter.action = 0, 6, 8

    @staticmethod
    def exit(hitter, e):
        pass

    @staticmethod
    def do(hitter):
        hitter.frame = (hitter.frame + 1) % hitter.frame_number

    @staticmethod
    def draw(hitter):
        draw_hitter(hitter)


class Hit:
    @staticmethod
    def enter(hitter, e):
        hitter.frame, hitter.frame_number, hitter.action = 0, 8, 9
        # hitter.user_force = (server.make_ui.action * 10 + server.make_ui.frame) / 100

    @staticmethod
    def exit(hitter, e):
        pass

    @staticmethod
    def do(hitter):
        hitter.frame = hitter.frame + 1
        if hitter.frame == 4:
            # hit = hitter.user_force + float(hitter.BA) * random.randint(0, 3)
            # hit = 0.6 # 항상 볼
            # hit = 0.3  # 항상 스트라이크
            hitter.hit = 1.1  # 항상 hit
            if hitter.hit > 1:
                hitter.strike, hitter.ball = 0, 0
                hitter.base = number_to_bases[attack_zone]
                game_world.update_handle_event(('HIT_SUCCESS', 0))
        if hitter.frame == hitter.frame_number:
            if hitter.hit > 1:
                # 원래 여기에 있는 게 맞긴 함
                # hitter.strike, hitter.ball = 0, 0
                # hitter.base = number_to_bases[attack_zone]
                hitter.state_machine.handle_event(('HIT_SUCCESS', 0))
            else:
                if hitter.hit < 0.4:
                    hitter.strike += 1
                else:
                    hitter.ball += 1
                if hitter.strike == 3:
                    print('STRIKE_3')
                    set_next_hitter(hitter)
                elif hitter.ball == 4:
                    print('BALL_4')
                    hitter.strike, hitter.ball = 0, 0
                    hitter.state_machine.handle_event(('FOUR_BALL', 0))
                    game_world.update_handle_event(('FOUR_BALL', 0))
                else:
                    hitter.state_machine.handle_event(('HIT_FAIL', 0))

    @staticmethod
    def draw(hitter):
        draw_hitter(hitter)


class HitterRun:
    @staticmethod
    def enter(hitter, e):
        hitter.frame, hitter.frame_number, hitter.action = 0, 8, 5

        # 현재 위치, 목표 위치, 매개 변수 t 정의
        hitter.current_position = hitter.base.pos  # base class
        hitter.goal_position = hitter.base.next_base  # 튜플 (x, y)
        hitter.t = 0.0

        number_to_bases[hitter.base.next_base].runners_goal_base = True

    @staticmethod
    def exit(hitter, e):
        pass

    @staticmethod
    def do(hitter):
        # 프레임 넘기기
        hitter.frame = (hitter.frame + 1) % hitter.frame_number

        # 직선 이동 방정식
        x = (1 - hitter.t) * hitter.current_position[0] + hitter.t * hitter.goal_position[0]
        y = (1 - hitter.t) * hitter.current_position[1] + hitter.t * hitter.goal_position[1]
        hitter.pos = (x, y)
        hitter.t += 0.1 * ((hitter.RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * PIXEL_PER_METER * game_framework.frame_time

        if hitter.t > 1:
            make_team.search_next_hitter(hitter)
            # 위치를 확실히 하기 위해 한 번 더 정의
            hitter.pos = hitter.goal_position

            # hitter의 base 업데이트 하기
            hitter.base = number_to_bases[hitter.base.next_base]
            hitter.base.hasRunner = True
            hitter.base.runners_goal_base = False
            hitter.init_state_machine('주자')

    @staticmethod
    def draw(hitter):
        draw_hitter(hitter)


class RunnerRun:
    @staticmethod
    def enter(hitter, e):
        hitter.frame, hitter.frame_number, hitter.action = 0, 8, 5

        # 현재 위치, 목표 위치, 매개 변수 t 정의
        hitter.current_position = hitter.base.pos
        hitter.goal_position = hitter.base.next_base
        hitter.t = 0.0

        hitter.base.hasRunner = False

        number_to_bases[hitter.base.next_base].runners_goal_base = True
        # if positions[positions[hitter.pos][2]][1] is False:
        #     hitter.state_machine.handle_event(('RUN_DONE', 0))

    @staticmethod
    def exit(hitter, e):
        # 위치를 확실히 하기 위해 한 번 더 정의
        hitter.pos = hitter.goal_position

        # hitter의 base 업데이트 하기
        hitter.base = number_to_bases[hitter.base.next_base]
        hitter.base.hasRunner = True
        hitter.base.runners_goal_base = False

        # home 에 도착한 경우,,,
        if hitter.base.pos == home:
            server.goal_runner = hitter
            game_world.remove_object(hitter)

    @staticmethod
    def do(hitter):
        # 프레임 넘기기
        hitter.frame = (hitter.frame + 1) % hitter.frame_number

        # 직선 이동 방정식
        x = (1 - hitter.t) * hitter.current_position[0] + hitter.t * hitter.goal_position[0]
        y = (1 - hitter.t) * hitter.current_position[1] + hitter.t * hitter.goal_position[1]
        hitter.pos = (x, y)
        hitter.t += 0.1 * ((
                                   hitter.RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * PIXEL_PER_METER * game_framework.frame_time

        # 직선 이동이 끝날 때 run_done 이벤트 발생
        if hitter.t > 1:
            hitter.state_machine.handle_event(('RUN_DONE', 0))

    @staticmethod
    def draw(hitter):
        draw_hitter(hitter)


class DefenderIdle:
    @staticmethod
    def enter(hitter, e):
        hitter.frame, hitter.frame_number, hitter.action = 0, 7, 4

    @staticmethod
    def exit(hitter, e):
        if e[0] == 'SUPER_CATCH':
            print('한 번에 잡음', hitter.name)
            set_next_hitter(server.cur_hitter)
            server.ball.state_machine.handle_event(('BACK_TO_MOUND', 0))
            # 수비수 (투수 제외)
            for o in game_world.objects[1][1:9]:
                if o.pos is not o.defence_position:
                    print('돌아감', o.name)
                    o.state_machine.handle_event(('BACK_TO_DEFENCE', 0))

    @staticmethod
    def do(hitter):
        hitter.frame = (hitter.frame + 1) % hitter.frame_number

    @staticmethod
    def draw(hitter):
        draw_hitter(hitter)


class RunToBall:
    @staticmethod
    def enter(hitter, e):
        hitter.frame, hitter.frame_number, hitter.action = 0, 7, 2

        # 현재 위치, 목표 위치, 매개 변수 t 정의
        hitter.current_position = hitter.pos
        hitter.goal_position = server.ball.goal_position
        hitter.t = 0.0

    @staticmethod
    def exit(hitter, e):
        if e[0] == 'SUPER_CATCH':
            print('한 번에 잡음', hitter.name)
            set_next_hitter(server.cur_hitter)
            server.ball.state_machine.handle_event(('BACK_TO_MOUND', 0))
            # 수비수 (투수 제외)
            for o in game_world.objects[1][1:9]:
                if o.pos is not o.defence_position:
                    print('돌아감', o.name)
                    o.state_machine.handle_event(('BACK_TO_DEFENCE', 0))
        elif e[0] == 'THROW_TO_NEAR_BASE':
            print('가까운 베이스로 보내기', hitter.name)
            server.ball.state_machine.handle_event(('THROW_TO_NEAR_BASE', hitter))
            # 수비수 (투수 제외)
            for o in game_world.objects[1][1:9]:
                if o.pos is not o.defence_position:
                    print('돌아감', o.name)
                    o.state_machine.handle_event(('BACK_TO_DEFENCE', 0))

    @staticmethod
    def do(hitter):
        # 프레임 넘기기
        hitter.frame = (hitter.frame + 1) % hitter.frame_number

        # 직선 이동 방정식
        x = (1 - hitter.t) * hitter.current_position[0] + hitter.t * hitter.goal_position[0]
        y = (1 - hitter.t) * hitter.current_position[1] + hitter.t * hitter.goal_position[1]
        hitter.pos = (x, y)
        hitter.t += 0.1 * ((hitter.RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * PIXEL_PER_METER * game_framework.frame_time

        # 직선 이동이 끝날 때 RUN_DONE 이벤트 발생
        if hitter.t > 1:
            hitter.state_machine.handle_event(('RUN_DONE', 0))

    @staticmethod
    def draw(hitter):
        draw_hitter(hitter)


class RunToDefencePos:
    @staticmethod
    def enter(hitter, e):
        hitter.frame, hitter.frame_number, hitter.action = 0, 7, 3

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
        hitter.t += 0.1 * ((hitter.RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * PIXEL_PER_METER * game_framework.frame_time

        # 직선 이동이 끝날 때 RUN_DONE 이벤트 발생
        if hitter.t > 1:
            hitter.state_machine.handle_event(('RUN_DONE', 0))

    @staticmethod
    def draw(hitter):
        draw_hitter(hitter)


## 상태 머신 ##
class StateMachineHitter:
    def __init__(self, hitter):
        self.hitter = hitter
        self.cur_state = HitterIdle
        self.transitions = {
            HitterIdle: {hit_start: Hit},
            Hit: {hit_success: HitterRun, hit_fail: HitterIdle, four_ball: HitterRun},
            HitterRun: {run_done: HitterIdle}
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


class StateMachineRunner:
    def __init__(self, hitter):
        self.hitter = hitter
        self.cur_state = RunnerIdle
        self.transitions = {
            RunnerIdle: {hit_success: RunnerRun, four_ball: RunnerRun},
            RunnerRun: {run_done: RunnerIdle}
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


class StateMachineDefender:
    def __init__(self, hitter):
        self.hitter = hitter

        self.cur_state = DefenderIdle
        self.transitions = {
            DefenderIdle: {hit_success: RunToBall, super_catch: RunToDefencePos, back_to_defence: RunToDefencePos},
            RunToBall: {run_done: DefenderIdle, super_catch: RunToDefencePos, throw_to_near_base: RunToDefencePos, back_to_defence: RunToDefencePos},
            RunToDefencePos: {run_done: DefenderIdle},
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


state_machines = {
    '주자': StateMachineRunner,
    '타자': StateMachineHitter,
    '수비수': StateMachineDefender
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
            Hitter.image = load_image('resource/image/animation.png')

        # 상태 머신 추가
        self.state_machine = None

    def set_team_color(self, color):
        if color == '파랑':
            self.team_color = 13
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
        sx, sy = self.pos[0] - server.background.window_left, self.pos[1] - server.background.window_bottom
        return sx - 20, sy - 30, sx + 20, sy + 30

    def handle_collision(self, group, other):
        if group == 'ball:defender' and other.is_collision is False:
            print('h', group, self.name)
            if other.state_machine.cur_state == obj_ball.Throw:
                print('한 번에 잡음')
                self.state_machine.handle_event(('SUPER_CATCH', 0))
                other.is_collision = True
            else:
                print('가까운 곳 보낼 거')
                self.state_machine.handle_event(('THROW_TO_NEAR_BASE', 0))
                other.is_collision = True

    def throw_to_base(self):
        for base in next_base[self.defence_position]:
            if number_to_bases[base].runners_goal_base:
                return base
        return home

    def run_to_ball(self, goal_pos):
        # x: 500 이상, y: 350 이상 > 중견수, 우익수
        if goal_pos[0] >= 500 and self.pos[0] >= 500 and goal_pos[1] >= 350 and self.pos[1] >= 350: return True
        # x: 500 이하, y: 350 이상 > 좌익수, 중견수
        if goal_pos[0] <= 500 and self.pos[0] <= 500 and goal_pos[1] >= 350 and self.pos[1] >= 350: return True
        # x: 500 이상, y: 350 이하 > 1루수, 2루수
        if goal_pos[0] >= 500 and self.pos[0] >= 500 and goal_pos[1] <= 350 and self.pos[1] <= 350: return True
        # x: 500 이하, y: 350 이하 > 유격수, 3루수
        if goal_pos[0] <= 500 and self.pos[0] <= 500 and goal_pos[1] <= 350 and self.pos[1] <= 350: return True
        return False
