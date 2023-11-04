from pico2d import load_image

## 상태머신 ##
class Idle:
    @staticmethod
    def enter():
        print('Idle Enter')

    @staticmethod
    def exit():
        print('Idle Exit')

    @staticmethod
    def do():
        print('Idle Do')

    @staticmethod
    def draw():
        pass


class StateMachine:
    def __init__(self):
        self.cur_state = Idle

    def start(self):
        self.cur_state.enter()

    def update(self):
        self.cur_state.do()

    def draw(self):
        self.cur_state.draw()

## 클래스 ##
class Hitter:
    image = None

    def __init__(self, x, y, name, hit, home_run, stolen_base, BA, OPS):
        # 위치, 현재 프레임, 현재 action, 프레임의 길이
        self.x, self.y = x, y
        self.frame, self.frame_number, self.action = 0, 1, 4
        # self.team_color = team_color

        # 파일: 이름, 안타, 홈런, 도루, 타율, 출루율 + 장타율
        self.name, self.hit, self.home_run, self.stolen_base, self.BA, self.OPS = name, hit, home_run, stolen_base, BA, OPS

        # 이미지 로드
        if Hitter.image is None:
            Hitter.image = load_image('resource/image/character_hitter.png')

        # 상태머신 추가
        self.state_machine = StateMachine()
        self.state_machine.start()

    def handle_event(self, event):
        pass

    def update(self):
        self.state_machine.update()
        # self.frame = (self.frame + 1) % self.frame_number

    def draw(self):
        self.state_machine.draw()
        # Hitter.image.clip_draw(self.frame * 50, self.action * 50, 50, 50, self.x, self.y)