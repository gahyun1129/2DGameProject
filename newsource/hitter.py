from pico2d import load_image

## 상태머신 ##
class Idle:
    @staticmethod
    def enter(hitter):
        # action 값은 파란, 빨간 팀 모두 같음
        # 나중에 draw 할 때 team_color 값을 더해서 색 구분 하자!
        hitter.frame, hitter.frame_number, hitter.action = 0, 1, 4
        print('Idle Enter')

    @staticmethod
    def exit(hitter):
        print('Idle Exit')

    @staticmethod
    def do(hitter):
        hitter.frame = (hitter.frame + 1) % hitter.frame_number
        # print('Idle Do')

    @staticmethod
    def draw(hitter):
        hitter.image.clip_draw(hitter.frame * 50, (hitter.action+hitter.team_color) * 50, 50, 50, hitter.x, hitter.y)


class StateMachine:
    def __init__(self, hitter):
        self.hitter = hitter
        self.cur_state = Idle

    def start(self):
        self.cur_state.enter(self.hitter)

    def update(self):
        self.cur_state.do(self.hitter)

    def draw(self):
        self.cur_state.draw(self.hitter)

## 클래스 ##
class Hitter:
    image = None

    def __init__(self, x, y, name, hit, home_run, stolen_base, BA, OPS):
        # 위치, 현재 프레임, 현재 action, 프레임의 길이
        self.x, self.y = x, y
        self.frame, self.frame_number, self.action = 0, 1, 4
        self.team_color = 0

        # 파일: 이름, 안타, 홈런, 도루, 타율, 출루율 + 장타율
        self.name, self.hit, self.home_run, self.stolen_base, self.BA, self.OPS = name, hit, home_run, stolen_base, BA, OPS

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

    def init_state_machine(self):
        # 객체를 따로 만들어 주었으므로, 상태 머신 시작을 다시 해야 함.
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def handle_event(self, event):
        pass

    def update(self):
        self.state_machine.update()
        # self.frame = (self.frame + 1) % self.frame_number

    def draw(self):
        self.state_machine.draw()
        # Hitter.image.clip_draw(self.frame * 50, self.action * 50, 50, 50, self.x, self.y)