mound = (400, 240)
one_base = (600, 270)
two_base = (400, 350)
two_base_player = (470, 330)
three_base = (200, 270)
home = (400, 150)
short = (330, 330)
left = (100, 390)
right = (700, 390)
center = (400, 470)
attack_zone = (370, 160)
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

bases = []


# def set_base():
#     b = Base(attack_zone, one_base, (0, 0))
#     bases.append(b)
#     b = Base(one_base, two_base, attack_zone)
#     b.hasDefender = False
#     bases.append(b)
#     b = Base(two_base, three_base, one_base)
#     bases.append(b)
#     b = Base(three_base, home, two_base)
#     bases.append(b)
#     b = Base(home, (0, 0), three_base)
#     bases.append(b)



