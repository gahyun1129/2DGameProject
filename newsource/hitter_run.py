import attack_mode
import game_framework
import game_world
import hitter
import game_world
from define import positions, home


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
            attack_mode.goal_runner = hitter
            game_world.remove_object(hitter)
        positions[hitter.pos][1] = True

    @staticmethod
    def do(hitterObj):
        # 프레임 넘기기
        hitterObj.frame = (hitterObj.frame + 1) % hitterObj.frame_number

        # 직선 이동 방정식
        x = (1 - hitterObj.t) * hitterObj.current_position[0] + hitterObj.t * hitterObj.goal_position[0]
        y = (1 - hitterObj.t) * hitterObj.current_position[1] + hitterObj.t * hitterObj.goal_position[1]
        hitterObj.pos = (x, y)
        hitterObj.t += 0.1 * ((hitterObj.RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * hitter.PIXEL_PER_METER * game_framework.frame_time

        # 직선 이동이 끝날 때 run_success 이벤트 발생
        if hitterObj.t > 1:
            hitterObj.state_machine.handle_event(('RUN_DONE', 0))

    @staticmethod
    def draw(hitter):
        hitter.image.clip_draw(hitter.frame * 50, (hitter.action + hitter.team_color) * 50, 50, 50, hitter.pos[0],
                               hitter.pos[1])


class StateMachineRun:
    def __init__(self, hitterObj):
        self.hitter = hitterObj
        self.cur_state = hitter.Idle
        self.transitions = {
            hitter.Idle: {hitter.hit_success: Run, hitter.four_ball: Run},
            Run: {hitter.run_done: hitter.Idle}
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
