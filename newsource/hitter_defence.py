import game_framework
import hitter
import attack_mode


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
    def do(hitter_run):
        # 프레임 넘기기
        hitter_run.frame = (hitter_run.frame + 1) % hitter_run.frame_number

        # 직선 이동 방정식
        x = (1 - hitter_run.t) * hitter_run.current_position[0] + hitter_run.t * hitter_run.goal_position[0]
        y = (1 - hitter_run.t) * hitter_run.current_position[1] + hitter_run.t * hitter_run.goal_position[1]
        hitter_run.pos = (x, y)
        hitter_run.t += 0.1 * ((hitter_run.RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * hitter.PIXEL_PER_METER * game_framework.frame_time

        # 직선 이동이 끝날 때 RUN_DONE 이벤트 발생
        if hitter_run.t > 1:
            hitter_run.state_machine.handle_event(('RUN_DONE', 0))
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
    def do(hitter_run):
        # 프레임 넘기기
        hitter_run.frame = (hitter_run.frame + 1) % hitter_run.frame_number

        # 직선 이동 방정식
        x = (1 - hitter_run.t) * hitter_run.current_position[0] + hitter_run.t * hitter_run.goal_position[0]
        y = (1 - hitter_run.t) * hitter_run.current_position[1] + hitter_run.t * hitter_run.goal_position[1]
        hitter_run.pos = (x, y)
        hitter_run.t += 0.1 * ((hitter_run.RUN_SPEED_KMPH * 1000.0 / 60.0) / 60.0) * hitter.PIXEL_PER_METER * game_framework.frame_time

        # 직선 이동이 끝날 때 RUN_DONE 이벤트 발생
        if hitter_run.t > 1:
            hitter_run.state_machine.handle_event(('RUN_DONE', 0))
        # print('Run Do')

    @staticmethod
    def draw(hitter):
        hitter.image.clip_draw(hitter.frame * 50, (hitter.action + hitter.team_color) * 50, 50, 50, hitter.pos[0],
                               hitter.pos[1])


class StateMachineDefence:
    def __init__(self, hitterObj):
        self.hitter = hitterObj

        self.cur_state = hitter.Idle
        self.transitions = {
            hitter.Idle: {hitter.hit_success: RunDefence},
            RunDefence: {hitter.run_done: RunPosition},
            RunPosition: {hitter.run_done: hitter.Idle},
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