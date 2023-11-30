from pico2d import draw_rectangle
import game_world

bases = []

mound = (500, 240)
one_base = (650, 320)
two_base = (500, 380)
two_base_player = (500 + 60, 370)
three_base = (350, 320)
home = (500, 120)
short = (500 - 60, 370)
left = (250, 580)
right = (750, 580)
center = (500, 700)
attack_zone = (470, 150)


# 현재 위치 : 다음 베이스, 현재 베이스에 player가 있는지, 전 베이스
positions = {
    attack_zone: [one_base, True, (0, 0)],
    one_base: [two_base, False, attack_zone],
    two_base: [three_base, False, one_base],
    three_base: [home, False, two_base],
    home: [(0, 0), False, three_base]
}


# 가까운 base 판단하기 위해 필요한 딕셔너리
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
        self.runners_goal_base = False

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


# attack_zone
b = Base((0, 0), attack_zone, one_base)
bases.append(b)
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
    attack_zone: bases[0],
    one_base: bases[1],
    two_base: bases[2],
    three_base: bases[3],
    home: bases[4]
}