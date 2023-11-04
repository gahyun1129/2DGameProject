import copy

import attack_mode
import game_world
from hitter import Hitter
from pitcher import Pitcher
from define import *
import random


hitters = []
pitchers = []


user_players = []
computer_players = []


def make_team():
    hitters_len = len(hitters)
    # 빨간 팀 - 컴퓨터 (기본 색)
    # 투수 랜덤으로 정하기
    p = copy.copy(pitchers[random.randint(0, len(pitchers) - 1)])
    computer_players.append(p)

    # 타자 랜덤으로 정하기
    r = random.randint(0, hitters_len)
    for i in range(0, 9):
        h = copy.copy(hitters[(r + i) % hitters_len])
        computer_players.append(h)

    # 파란 팀 - 유저
    # 투수 랜덤으로 정하기
    p = copy.copy(pitchers[random.randint(0, len(pitchers) - 1)])
    p.action += 1
    user_players.append(p)

    # 타자 랜덤으로 정하기
    r = random.randint(0, hitters_len)
    for i in range(0, 9):
        h = copy.copy(hitters[(r + i) % hitters_len])
        h.action += 1
        user_players.append(h)


def set_player_from_data_file():
    file_path = 'resource/txt/Hitter.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        x, y = 300, 100
        for content in file:
            content = content.strip().split()
            name, hit, home_run, stolen_base, BA, OPS = content[0], content[1], content[2], content[3], content[4], \
                content[5]
            hitters.append(Hitter(x, y, name, hit, home_run, stolen_base, BA, OPS))

    file_path = 'resource/txt/Pitcher.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        x, y = 600, 100
        for content in file:
            content = content.strip().split()
            name, strike_out, four_balls, ERA, pitching = content[0], content[1], content[2], content[3], \
                [content[4], content[5], content[6]]
            pitchers.append(Pitcher(x, y, name, strike_out, four_balls, ERA, pitching))


def attack_position():
    (computer_players[0].x, computer_players[0].y) = mound
    (computer_players[1].x, computer_players[1].y) = one_base
    (computer_players[2].x, computer_players[2].y) = (two_base[0] + 70, two_base[1] - 20)
    (computer_players[3].x, computer_players[3].y) = three_base
    (computer_players[4].x, computer_players[4].y) = home
    (computer_players[5].x, computer_players[5].y) = short
    (computer_players[6].x, computer_players[6].y) = left
    (computer_players[7].x, computer_players[7].y) = right
    (computer_players[8].x, computer_players[8].y) = center

    attack_mode.cur_hitter = user_players[1]
    (attack_mode.cur_hitter.x, attack_mode.cur_hitter.y) = attack_zone

    game_world.add_layer(computer_players[0:9])
    game_world.add_layer([attack_mode.cur_hitter])
