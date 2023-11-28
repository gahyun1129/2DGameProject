from pico2d import draw_rectangle
import game_world

bases = []
number_to_bases = {}

mound = (400, 240)
one_base = (600, 270)
two_base = (400, 350)
two_base_player = (470, 330)
three_base = (200, 270)
home = (400, 120)
short = (330, 330)
left = (100, 390)
right = (700, 390)
center = (400, 470)
attack_zone = (370, 130)
ball = None

# 현재 위치 : 다음 베이스, 현재 베이스에 player가 있는지, 전 베이스
positions = {
    attack_zone: [one_base, True, (0, 0)],
    one_base: [two_base, False, attack_zone],
    two_base: [three_base, False, one_base],
    three_base: [home, False, two_base],
    home: [(0, 0), False, three_base]
}

next_base = {
    short: [two_base, three_base, home, one_base],
    left: [two_base, three_base, home, one_base],
    right: [two_base, one_base, home, three_base],
    center: [two_base, three_base, one_base, home],
    one_base: [one_base, two_base, home, three_base],
    two_base_player: [two_base, one_base, home, three_base],
    three_base: [three_base, two_base, home, one_base],
    home: [home]
}


class Base:
    def __init__(self, prev_base, pos, next_base):
        self.pos = pos
        self.hasDefender = True
        self.isFilled = False
        self.next_base = next_base
        self.prev_base = prev_base
        self.hasRunner = False

    def update(self):
        pass

    def draw(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.pos[0] - 10, self.pos[1] - 10, self.pos[0] + 10, self.pos[1] + 10

    def handle_collision(self, group, other):
        if group == 'hitter:base':
            self.hasRunner = True
        elif group == 'base:defender':
            self.hasDefender = True


def set_base():
    global number_to_bases
    # one_base
    b = Base(attack_zone, one_base, two_base)
    bases.append(b)
    # two_base
    b = Base(one_base, two_base, three_base)
    b.hasDefender = False
    bases.append(b)
    # three_base
    b = Base(two_base, three_base, home)
    bases.append(b)
    # home
    b = Base(three_base, home, (0, 0))
    bases.append(b)

    game_world.add_objects(bases, 4)

    number_to_bases = {
        one_base: bases[0],
        two_base: bases[1],
        three_base: bases[2],
        home: bases[3]
    }
