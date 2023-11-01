from player import Player


class Idle:
    @staticmethod
    def enter():
        print('Idle enter')

    @staticmethod
    def exit():
        print('Idle exit')

    @staticmethod
    def do():
        print('Idle do')

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


class Hitter(Player):
    def __init__(self, x, y, action, dir, frame_number, name, hit, home_run, stolen_base, BA, OPS):
        # 부모의 생성자 물려 받음.
        super().__init__(x, y, action, dir, frame_number, name)

        # 안타, 홈런, 도루, 타율, 출루율 + 장타율
        self.hit, self.home_run, self.stolen_base, self.BA, self.OPS = hit, home_run, stolen_base, BA, OPS
        self.state_machine = StateMachine()
        self.state_machine.start()

    def draw(self):
        if self.is_draw is True:
            self.state_machine.draw()

    def update(self):
        self.state_machine.update()

    def run_next_base(self, start, end):
        pass
