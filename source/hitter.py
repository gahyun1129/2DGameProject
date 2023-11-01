from player import Player


class Idle:
    @staticmethod
    def enter(hitter):
        hitter.action = 0
        hitter.frame = 0

    @staticmethod
    def exit(hitter):
        print('Idle exit')

    @staticmethod
    def do(hitter):
        hitter.frame = (hitter.frame + 1) % 6

    @staticmethod
    def draw(hitter):
        hitter.image.clip_draw(hitter.frame * 50, hitter.action * 50, 50, 50, hitter.x, hitter.y)


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


class Hitter(Player):
    def __init__(self, x, y, action, dir, frame_number, name, hit, home_run, stolen_base, BA, OPS):
        # 부모의 생성자 물려 받음.
        super().__init__(x, y, action, dir, frame_number, name)

        # 안타, 홈런, 도루, 타율, 출루율 + 장타율
        self.hit, self.home_run, self.stolen_base, self.BA, self.OPS = hit, home_run, stolen_base, BA, OPS
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def draw(self):
        if self.is_draw is True:
            self.state_machine.draw()

    def update(self):
        self.state_machine.update()

    def run_next_base(self, start, end):
        pass
