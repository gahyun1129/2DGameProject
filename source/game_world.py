# 게임 월드 관리 모듈
# 게임의 Object 관리

from player import Pitcher, Hitter
import make_team

hitter_player_list = []
pitcher_player_list = []


player = []


objects = [[]]


def add_object(o, depth=0):
    objects[depth].append(o)


def add_objects(ol, depth=0):
    objects[depth] += ol


def update():
    for layer in objects:
        for o in layer:
            o.update()


def render():
    for layer in objects:
        for o in layer:
            o.draw()


def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in objects:
        layer.clear()           # layer type은 list이므로


def set_player_list_from_data_file():
    file_path = 'resource/txt/Hitter.txt'

    with open(file_path, 'r', encoding='utf-8') as file:
        x, y, action, dir, frame_number = 400, 70, 0, 0, 6
        for content in file:
            content = content.strip().split()
            name, hit, home_run, stolen_base, BA, OPS = content[0], content[1], content[2], content[3], content[4], \
                content[5]
            hitter_player_list.append(Hitter(x, y, action, dir, frame_number, name, hit, home_run, stolen_base, BA, OPS))

    file_path = 'resource/txt/Pitcher.txt'

    with open(file_path, 'r', encoding='utf-8') as file:
        x, y, action, dir, frame_number = 600, 70, 0, 0, 8
        for content in file:
            content = content.strip().split()
            name, strike_out, four_balls, ERA, pitching = content[0], content[1], content[2], content[3], [content[4], content[5], content[6]]
            pitcher_player_list.append(Pitcher(x, y, action, dir, frame_number, name, strike_out, four_balls, ERA, pitching))

    make_team.make_team()

    add_objects(player, 0)

