from pico2d import load_image, load_font, draw_rectangle, load_music, load_wav

import game_framework
import server
import random

import mode.result_mode as result_mode
import mode.attack_mode as attack_mode
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


def to_catch_ball(e):
    return e[0] == 'TO_CATCH_BALL'


def draw_hitter(hitter):
    sx, sy = hitter.pos[0] - server.background.window_left, hitter.pos[1] - server.background.window_bottom
    hitter.image.clip_draw(hitter.frame * 100, (hitter.action + hitter.team_color) * 100, 100, 100, sx, sy)


def set_next_hitter(hitter):
    hitter.strike, hitter.ball = 0, 0
    make_team.search_next_hitter(server.cur_hitter)
    game_world.remove_object(hitter)
    if server.out_count == 3:
        out_situation()


def out_situation():
    server.out_count = 0
    server.cur_inning_turn = (server.cur_inning_turn + 1) % 2  # turn = 0: attack_mode, 초 turn = 1: defence_mode, 말
    if server.cur_inning_turn == 0:
        server.cur_inning += 1
    if server.cur_inning == 10:
        server.game_status = 'end'
        print('게임 끝!!!!!!!')
        # game_framework.change_mode(result_mode)
        # 나중에 여기서 결과 모드로 바꾸면 될 듯
    else:
        server.ui_inning.frame = server.cur_inning - 1
        server.ui_inning.size = 1
        if server.cur_inning_turn == 0:
            server.ui_inning.turn = 3
            game_framework.change_mode(attack_mode)
            server.ui_hitter_info.hitter_image = load_image('resource/image/hitter_red.png')
        else:
            server.ui_inning.turn = 2
            game_framework.change_mode(defence_mode)
            server.ui_hitter_info.hitter_image = load_image('resource/image/hitter_blue.png')


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
    def enter(runner, e):
        runner.frame, runner.frame_number, runner.action = 0, 6, 8

    @staticmethod
    def exit(runner, e):
        pass

    @staticmethod
    def do(runner):
        runner.frame = (runner.frame + 1) % runner.frame_number

    @staticmethod
    def draw(runner):
        draw_hitter(runner)


class Hit:
    @staticmethod
    def enter(hitter, e):
        hitter.frame, hitter.frame_number, hitter.action = 0, 8, 9
        hitter.user_force = server.progress_bar.frame * 0.01 + (server.progress_bar.action % 3) * 0.1
        # hitter.hit = hitter.user_force + float(hitter.BA) * random.randint(0, 3)
        # hitter.hit = 0.6 # 항상 볼
        # hitter.hit = 0.3  # 항상 스트라이크
        hitter.hit = 1.1  # 항상 hit

    @staticmethod
    def exit(hitter, e):
        pass

    @staticmethod
    def do(hitter):
        if hitter.hit > 1:  # hit 성공
            hitter.frame = hitter.frame + 1
            if hitter.frame == 4:  # 배트 돌리는 장면의 frame: 4
                game_world.update_handle_event(('HIT_SUCCESS', 0))  # 공과 수비수들은 각자의 자리를 향해 뜀
                server.ui_ment.draw_ment_ui('hit')  # hit ui 출력
                hitter.hit_sound.play()
            if hitter.frame == hitter.frame_number:
                hitter.strike, hitter.ball = 0, 0
                hitter.state_machine.handle_event(('HIT_SUCCESS', 0))  # 타자는 1루를 향해 뜀
        elif hitter.hit > 0.4:  # ball의 경우
            if server.ball.pos == home:
                hitter.ball += 1  # ball 개수 추가
                server.ui_ment.draw_ment_ui('ball', hitter.ball)  # ball ui 출력
                if hitter.ball == 4:  # 4 ball인 경우
                    hitter.strike, hitter.ball = 0, 0
                    for runner in game_world.objects[2]:
                        runner.state_machine.handle_event(('FOUR_BALL', 0))  # 타자와 주자는 1루를 향해 뜀
                server.progress_bar.frame = 0
                server.progress_bar.action = 0
                server.progress_bar.is_hit = False
                hitter.state_machine.handle_event(('HIT_FAIL', 0))
        else:  # strike의 경우
            if server.ball.pos == home:
                hitter.strike += 1  # strike 개수 추가
                server.ui_ment.draw_ment_ui('strike', hitter.strike)  # strike ui 출력
                if hitter.strike == 3:  # 3 스트라이크인 경우
                    server.out_count += 1
                    server.ui_judge.draw_judge_ui('out', server.out_count)  # 아웃 ui 출력
                    set_next_hitter(hitter)  # 현재 타자 삭제 후 다음 타자 렌더링
                server.progress_bar.frame = 0
                server.progress_bar.action = 0
                server.progress_bar.is_hit = False
                hitter.state_machine.handle_event(('HIT_FAIL', 0))

    @staticmethod
    def draw(hitter):
        draw_hitter(hitter)


class HitterRun:
    @staticmethod
    def enter(hitter, e):
        hitter.frame, hitter.frame_number, hitter.action = 0, 8, 5

        # 현재 위치, 목표 위치, 매개 변수 t 정의
        hitter.current_position = attack_zone
        hitter.goal_position = one_base
        hitter.t = 0.0

        number_to_bases[one_base].will_be_filled = True
        number_to_bases[one_base].cur_runner = hitter

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
            # 위치를 확실히 하기 위해 한 번 더 정의
            hitter.pos = hitter.goal_position

            make_team.search_next_hitter(hitter)

            # hitter의 base 업데이트 하기
            if hitter.base.cur_runner == hitter:
                hitter.base.cur_runner = None
            hitter.base = number_to_bases[one_base]
            hitter.base.has_runner = True
            hitter.base.will_be_filled = False
            hitter.init_state_machine('주자')

    @staticmethod
    def draw(hitter):
        draw_hitter(hitter)


class RunnerRun:
    @staticmethod
    def enter(runner, e):
        runner.frame, runner.frame_number, runner.action = 0, 8, 5

        # 현재 위치, 목표 위치, 매개 변수 t 정의
        runner.current_position = runner.base.pos
        runner.goal_position = runner.base.next_base
        runner.t = 0.0

        runner.pass_ = False

        if runner.base.cur_runner == runner:
            runner.base.cur_runner = None

        number_to_bases[runner.base.next_base].will_be_filled = True
        number_to_bases[runner.base.next_base].cur_runner = runner

        # four ball 경우 전 베이스에 주자가 없었다면 뛰지 않음.
        if e[0] == 'FOUR_BALL' and not number_to_bases[runner.base.prev_base].has_runner:
            runner.state_machine.handle_event(('RUN_DONE', 0))
            runner.pass_ = True

    @staticmethod
    def exit(runner, e):
        if not runner.pass_:
            # 위치를 확실히 하기 위해 한 번 더 정의
            runner.pos = runner.goal_position

            # runner base 업데이트 하기
            if runner.base.cur_runner == runner:
                runner.base.cur_runner = None
            runner.base = number_to_bases[runner.base.next_base]
            runner.base.has_runner = True
            runner.base.will_be_filled = False

            # home 에 도착한 경우,,,
            if runner.base.pos == home:
                # goal_runner 말고 점수 업데이트 해 줘야 할 것 같다...
                if server.cur_inning_turn == 0:
                    server.user_score += 1
                else:
                    server.com_score += 1
                game_world.remove_object(runner)

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
    def enter(defender, e):
        defender.frame, defender.frame_number, defender.action = 0, 7, 4

    @staticmethod
    def exit(defender, e):
        if e[0] == 'SUPER_CATCH':
            print('아이들 상태, 한 번에 잡음', defender.name)
            server.out_count += 1
            server.ui_judge.draw_judge_ui('out', server.out_count)  # 아웃 ui 출력
            set_next_hitter(server.cur_hitter)
            server.ball.state_machine.handle_event(('BACK_TO_MOUND', 0))
            # 수비수 (투수 제외)
            for o in game_world.objects[1][2:9]:
                if o.pos is not o.defence_position:
                    print('돌아감', o.name)
                    o.state_machine.handle_event(('BACK_TO_DEFENCE', 0))
        elif e[0] == 'THROW_TO_NEAR_BASE':
            print('아이들 상태, 가까운 베이스로 보내기', defender.name)
            server.ball.state_machine.handle_event(('THROW_TO_NEAR_BASE', defender))
            # 수비수 (투수 제외)
            for o in game_world.objects[1][2:9]:
                if o.pos is not o.defence_position:
                    o.state_machine.handle_event(('TO_CATCH_BALL', 0))
                    print('돌아감', o.name)
                    # o.state_machine.handle_event(('BACK_TO_DEFENCE', 0))

    @staticmethod
    def do(defender):
        defender.frame = (defender.frame + 1) % defender.frame_number

    @staticmethod
    def draw(defender):
        draw_hitter(defender)


class RunToBall:
    @staticmethod
    def enter(defender, e):
        defender.frame, defender.frame_number, defender.action = 0, 7, 2

        # 현재 위치, 목표 위치, 매개 변수 t 정의
        defender.current_position = defender.pos
        defender.goal_position = server.ball.goal_position
        defender.t = 0.0

    @staticmethod
    def exit(defender, e):
        if e[0] == 'SUPER_CATCH':
            print('run 상태, 한 번에 잡음', defender.name)
            server.out_count += 1
            server.ui_judge.draw_judge_ui('out', server.out_count)  # 아웃 ui 출력
            set_next_hitter(server.cur_hitter)
            server.ball.state_machine.handle_event(('BACK_TO_MOUND', 0))
            # 수비수 (투수 제외)
            for o in game_world.objects[1][2:9]:
                if o.pos is not o.defence_position:
                    print('한 번에 잡아서 돌아감', o.name)
                    o.state_machine.handle_event(('BACK_TO_DEFENCE', 0))
        elif e[0] == 'THROW_TO_NEAR_BASE':
            print('run 상태, 가까운 베이스로 보내기', defender.name)
            server.ball.state_machine.handle_event(('THROW_TO_NEAR_BASE', defender))
            # 수비수 (투수 제외)
            for o in game_world.objects[1][2:9]:
                if o.pos is not o.defence_position:
                    print('공 잡으러 감', o.name)
                    o.state_machine.handle_event(('TO_CATCH_BALL', 0))

    @staticmethod
    def do(defender):
        # 프레임 넘기기
        defender.frame = (defender.frame + 1) % defender.frame_number

        # 직선 이동 방정식
        x = (1 - defender.t) * defender.current_position[0] + defender.t * defender.goal_position[0]
        y = (1 - defender.t) * defender.current_position[1] + defender.t * defender.goal_position[1]
        defender.pos = (x, y)
        defender.t += 0.1 * (
                    (defender.RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * PIXEL_PER_METER * game_framework.frame_time

        # 직선 이동이 끝날 때 RUN_DONE 이벤트 발생
        if defender.t > 1:
            defender.state_machine.handle_event(('RUN_DONE', 0))

    @staticmethod
    def draw(defender):
        draw_hitter(defender)


class RunToDefencePos:
    @staticmethod
    def enter(defender, e):
        defender.frame, defender.frame_number, defender.action = 0, 7, 3

        # 현재 위치, 목표 위치, 매개 변수 t 정의
        defender.current_position = defender.pos
        defender.goal_position = defender.defence_position
        defender.t = 0.0

    @staticmethod
    def exit(defender, e):
        # 위치를 확실히 하기 위해 한 번 더 정의
        defender.pos = defender.defence_position

    @staticmethod
    def do(defender):
        # 프레임 넘기기
        defender.frame = (defender.frame + 1) % defender.frame_number

        # 직선 이동 방정식
        x = (1 - defender.t) * defender.current_position[0] + defender.t * defender.goal_position[0]
        y = (1 - defender.t) * defender.current_position[1] + defender.t * defender.goal_position[1]
        defender.pos = (x, y)
        defender.t += 0.1 * (
                    (defender.RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * PIXEL_PER_METER * game_framework.frame_time

        # 직선 이동이 끝날 때 RUN_DONE 이벤트 발생
        if defender.t > 1:
            defender.state_machine.handle_event(('RUN_DONE', 0))

    @staticmethod
    def draw(defender):
        draw_hitter(defender)


class DefenderCatchBall:
    @staticmethod
    def enter(defender, e):
        if defender.run_to_catch_ball:
            defender.frame, defender.frame_number, defender.action = 0, 7, 3

            # 현재 위치, 목표 위치, 매개 변수 t 정의
            defender.current_position = defender.pos
            defender.goal_position = server.ball.goal_position
            defender.t = 0.0
        else:
            defender.state_machine.handle_event(('BACK_TO_DEFENCE', 0))

    @staticmethod
    def exit(defender, e):
        pass
        # 위치를 확실히 하기 위해 한 번 더 정의
        # defender.pos = defender.goal_position

    @staticmethod
    def do(defender):
        # 프레임 넘기기
        defender.frame = (defender.frame + 1) % defender.frame_number

        # 직선 이동 방정식
        x = (1 - defender.t) * defender.current_position[0] + defender.t * defender.goal_position[0]
        y = (1 - defender.t) * defender.current_position[1] + defender.t * defender.goal_position[1]
        defender.pos = (x, y)
        defender.t += 0.1 * (
                    (defender.RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * PIXEL_PER_METER * game_framework.frame_time

        # 직선 이동이 끝날 때 RUN_DONE 이벤트 발생
        if defender.t > 1:
            defender.state_machine.handle_event(('RUN_DONE', 0))

    @staticmethod
    def draw(defender):
        draw_hitter(defender)


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
        sx, sy = self.hitter.pos[0] - server.background.window_left, self.hitter.pos[
            1] - server.background.window_bottom


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
        sx, sy = self.hitter.pos[0] - server.background.window_left, self.hitter.pos[
            1] - server.background.window_bottom
        self.hitter.font.draw(sx - 10, sy + 50, f'{self.hitter.name}', (0, 0, 255))


class StateMachineDefender:
    def __init__(self, hitter):
        self.hitter = hitter

        self.cur_state = DefenderIdle
        self.transitions = {
            DefenderIdle: {hit_success: RunToBall, super_catch: RunToDefencePos, back_to_defence: RunToDefencePos,
                           throw_to_near_base: RunToDefencePos, to_catch_ball: DefenderCatchBall},
            RunToBall: {run_done: DefenderIdle, super_catch: RunToDefencePos, throw_to_near_base: RunToDefencePos,
                        back_to_defence: RunToDefencePos, to_catch_ball: DefenderCatchBall},
            RunToDefencePos: {run_done: DefenderIdle},
            DefenderCatchBall: {run_done: DefenderIdle, back_to_defence: RunToDefencePos}
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
        sx, sy = self.hitter.pos[0] - server.background.window_left, self.hitter.pos[
            1] - server.background.window_bottom
        self.hitter.font.draw(sx - 10, sy + 50, f'{self.hitter.name}', (255, 255, 0))


class CatcherIdle:
    @staticmethod
    def enter(runner, e):
        runner.frame, runner.frame_number, runner.action = 0, 5, 0

    @staticmethod
    def exit(runner, e):
        pass

    @staticmethod
    def do(runner):
        runner.frame = (runner.frame + 1) % runner.frame_number

    @staticmethod
    def draw(runner):
        draw_hitter(runner)


class StateMachineCatcher:
    def __init__(self, hitter):
        self.hitter = hitter

        self.cur_state = CatcherIdle
        self.transitions = {
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


state_machines = {
    '주자': StateMachineRunner,
    '타자': StateMachineHitter,
    '수비수': StateMachineDefender,
    '포수': StateMachineCatcher
}


## 클래스 ##
class Hitter:
    image = None
    hit_sound = None
    defence_sound = None

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
        self.strike, self.ball = 0, 0

        # 타자의 달리기 속도
        self.RUN_SPEED_KMPH = random.randint(4, 8) / 10

        # 수비수의 base 위치
        self.base = None

        # 이미지 로드
        if Hitter.image is None:
            Hitter.image = load_image('resource/image/animation.png')
            Hitter.hit_sound = load_wav('resource/sound/hitsound.wav')
            Hitter.hit_sound.set_volume(32)

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
            if number_to_bases[base].will_be_filled:
                return base
        return one_base

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

    def run_to_catch_ball(self, goal_pos):
        if goal_pos[0] - 200 <= self.pos[0] <= goal_pos[0] + 200 \
                and goal_pos[1] - 200 <= self.pos[1] <= goal_pos[1] + 200:
            return True
        return False
