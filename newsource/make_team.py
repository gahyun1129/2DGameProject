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
    # 투수 랜덤 으로 정하기
    p = copy.copy(pitchers[random.randint(0, len(pitchers) - 1)])
    computer_players.append(p)

    # 타자 랜덤 으로 정하기
    r = random.randint(0, hitters_len)
    for i in range(0, 9):
        h = copy.copy(hitters[(r + i) % hitters_len])
        computer_players.append(h)

    # 파란 팀 - 유저
    # 투수 랜덤 으로 정하기
    p = copy.copy(pitchers[random.randint(0, len(pitchers) - 1)])
    p.action += 1
    user_players.append(p)

    # 타자 랜덤 으로 정하기
    r = random.randint(0, hitters_len)
    for i in range(0, 9):
        h = copy.copy(hitters[(r + i) % hitters_len])
        h.set_team_color('파랑')
        user_players.append(h)


def set_player_from_data_file():
    file_path = 'resource/txt/Hitter.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        pos = (300, 100)
        for content in file:
            content = content.strip().split()
            name, hit, home_run, stolen_base, BA, OPS = content[0], content[1], content[2], content[3], content[4], \
                content[5]
            hitters.append(Hitter(pos, name, hit, home_run, stolen_base, BA, OPS))

    file_path = 'resource/txt/Pitcher.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        pos = (600, 100)
        for content in file:
            content = content.strip().split()
            name, strike_out, four_balls, ERA, pitching = content[0], content[1], content[2], content[3], \
                [content[4], content[5], content[6]]
            pitchers.append(Pitcher(pos, name, strike_out, four_balls, ERA, pitching))


def attack_position():
    # com 팀 투수의 위치 잡기
    computer_players[0].pos = mound

    # com 팀 타자 중 8명의 수비 위치 잡기
    computer_players[1].pos = one_base
    computer_players[2].pos = (two_base[0] + 70, two_base[1] - 20)
    computer_players[3].pos = three_base
    computer_players[4].pos = home
    computer_players[5].pos = short
    computer_players[6].pos = left
    computer_players[7].pos = right
    computer_players[8].pos = center

    # user 팀 1번 타자의 공격 위치 잡기
    attack_mode.cur_hitter = user_players[1]
    attack_mode.cur_hitter.pos = attack_zone

    # com 팀 투수 1명과 타자 8명 game_world list 에 넣어 렌더링 하기
    # game_world.objects[1]
    game_world.add_layer(computer_players[0:9])

    # user 팀 1번 타자 game_world list 에 넣어 렌더링 하기
    # game_world.objects[2]
    game_world.add_layer([attack_mode.cur_hitter])

    # state_machine 구동 하기
    # 일단은 pitcher 상태 머신 구현 하기 전이니, hitter 만 구동함.
    # '인자' 의 값에 따라서 다른 타입의 상태 머신 작동.
    for o in game_world.objects[1]:
        o.init_state_machine('수비수')

    for o in game_world.objects[2]:
        o.init_state_machine('타자')


def set_next_hitter(hitter):
    # 다음 타자의 index 찾기
    # 만약 index 가 list 의 최대 값인 9를 넘거나, 투수의 번호인 0이 아니게 1로 변경함.
    next_hitter_index = user_players.index(hitter) + 1
    if next_hitter_index > 10:
        next_hitter_index = 1
    cur_hitter = user_players[next_hitter_index]
    cur_hitter.pos = attack_zone
    cur_hitter.init_state_machine('타자')
    game_world.add_object(cur_hitter, 2)
    attack_mode.cur_hitter = cur_hitter
