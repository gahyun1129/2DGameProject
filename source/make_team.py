# 나중에 이름을 lobby_mode로 바꿀 예정
# 현재 기능: 파일에서 선수 목록을 읽어 오고, random으로 경기에 참여할 팀원 결정
# 투수 중 1명 타자 9명, 투수는 항상 player 리스트의 1번 요소일 것
from hitter import Hitter
from pitcher import Pitcher

import game_world
import random


hitter_player = []
pitcher_player = []

user_players = []
com_players = []


def make_team():

    # 파란 팀
    l = len(hitter_player)

    # 투수 랜덤으로 정하기
    user_players.append(pitcher_player[random.randint(0, len(pitcher_player) - 1)])

    # 타자 랜덤으로 정하기
    r = random.randint(0, l)
    for i in range(0, 1):
        user_players.append(hitter_player[(r + i) % l])


    # 빨간 팀
    # 투수 랜덤으로 정하기
    com_players.append(
        pitcher_player[random.randint(0, len(pitcher_player) - 1)])

    # 타자 랜덤으로 정하기
    r = random.randint(0, l)
    for i in range(0, 9):
        com_players.append(hitter_player[(r + i) % l])


def set_player_list_from_data_file():
    file_path = 'resource/txt/Hitter.txt'

    with open(file_path, 'r', encoding='utf-8') as file:
        x, y, action, dir, frame_number = 400, 70, 4, 0, 1
        for content in file:
            content = content.strip().split()
            name, hit, home_run, stolen_base, BA, OPS = content[0], content[1], content[2], content[3], content[4], \
                content[5]
            hitter_player.append(Hitter(x, y, action, dir, frame_number, name, hit, home_run, stolen_base, BA, OPS))

    file_path = 'resource/txt/Pitcher.txt'

    with open(file_path, 'r', encoding='utf-8') as file:
        x, y, action, dir, frame_number = 600, 70, 0, 0, 1
        for content in file:
            content = content.strip().split()
            name, strike_out, four_balls, ERA, pitching = content[0], content[1], content[2], content[3], \
                [content[4], content[5], content[6]]
            pitcher_player.append(Pitcher(x, y, action, dir, frame_number, name, strike_out, four_balls, ERA, pitching))

    make_team()

    # game_world.add_objects(user_players, 1)
    # game_world.add_objects(com_players, 0)



