from sdl2 import SDL_KEYDOWN, SDLK_SPACE
from pico2d import load_image
from player import Player


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):
    return e[0] == 'TIME_OUT'


class Idle:
    @staticmethod
    def enter(hitter, e):
        # 전 타자의 타석이 끝나고 변경되었을 때 히트 게이지를 맞추고 있을 때 플레이됨
        # enter action으로 변경, frame = 0으로 초기화
        hitter.action = 5
        hitter.frame = 0

        hitter.image = load_image('resource/image/idle.png')

    @staticmethod
    def exit(hitter, e):
        # user가 space를 누를 때 exit됨
        print('Idle exit')

    @staticmethod
    def do(hitter):
        # 프레임 업데이트
        hitter.frame = (hitter.frame + 1) % 1

    @staticmethod
    def draw(hitter):
        # idle 이미지 무한 로딩
        Player.image.clip_draw(hitter.frame * 50, hitter.action * 50, 50, 50, hitter.x, hitter.y)


class Hit:
    @staticmethod
    def enter(hitter, e):
        # 스페이스 바를 눌렀을 때 플레이됨.
        hitter.action = 2
        hitter.frame = 0
        print('Hit enter')

    @staticmethod
    def exit(hitter, e):
        # 방망이 한 바퀴 흔들었을 때 끝남
        # 만일, 스트라이크, 실패 시엔 다시 돌아와야 함. boy의 fire_ball같이
        # 스트라이크가 3번 쌓이면 아예 모드를 바꿀 거임
        print('Hit exit')

    @staticmethod
    def do(hitter):
        # 프레임 업데이트 프레임이 한 바퀴 돌면 끝남
        hitter.action = (hitter.action + 1)
        if hitter.action == 5:
            hitter.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(hitter):
        # 휘두르는 애니메이션 출력
        Player.image.clip_draw(hitter.frame * 50, hitter.action * 50, 50, 50, hitter.x, hitter.y)


class StateMachine:
    def __init__(self, hitter):
        self.hitter = hitter
        self.cur_state = Idle
        self.transitions = {
            Idle: {space_down: Hit},
            Hit: {time_out: Idle}
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


class Hitter(Player):
    def __init__(self, x, y, action, dir, frame_number, name, hit, home_run, stolen_base, BA, OPS):
        # 부모의 생성자 물려 받음.
        super().__init__(x, y, action, dir, frame_number, name)

        # 안타, 홈런, 도루, 타율, 출루율 + 장타율
        self.hit, self.home_run, self.stolen_base, self.BA, self.OPS = hit, home_run, stolen_base, BA, OPS
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def draw(self):
        self.state_machine.draw()

    def update(self):
        self.state_machine.update()

    def run_next_base(self, start, end):
        pass

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))