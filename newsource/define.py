from base import Base

mound = (400, 240)
one_base = (600, 270)
two_base = (400, 350)
three_base = (200, 270)
home = (400, 150)
short = (330, 330)
left = (100, 390)
right = (700, 390)
center = (400, 470)
attack_zone = (370, 160)
ball = None

positions = {
    attack_zone: one_base,
    one_base: two_base,
    two_base: three_base,
    three_base: home,
    home: (0, 0)
}


def set_base():
    return [Base(base, next_base) for base, next_base in positions.items()]
