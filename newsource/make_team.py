from hitter import Hitter
from pitcher import Pitcher
import random


hitters = []
pitchers = []


user_players = []
computer_players = []

def make_team():
    # 파란 팀
    hitters_len = len(hitters)

    # 투수 랜덤으로 정하기
    p = pitchers[random.randint(0, len(pitchers) - 1)]
    p.action += 1
    user_players.append(p)

    # 타자 랜덤으로 정하기
    r = random.randint(0, hitters_len)
    for i in range(0, 9):
        h = hitters[(r + i) % hitters_len]
        h.action += 1
        user_players.append(h)

    # 빨간 팀
    # 투수 랜덤으로 정하기
    computer_players.append(
        pitchers[random.randint(0, len(pitchers) - 1)])

    # 타자 랜덤으로 정하기
    r = random.randint(0, hitters_len)
    for i in range(0, 9):
        computer_players.append(hitters[(r + i) % hitters_len])


def set_player_from_data_file():
    file_path = 'resource/txt/Hitter.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        x, y, frame_number, action = 300, 100, 1, 4
        for content in file:
            content = content.strip().split()
            name, hit, home_run, stolen_base, BA, OPS = content[0], content[1], content[2], content[3], content[4], \
                content[5]
            hitters.append(Hitter(x, y, frame_number, action, name, hit, home_run, stolen_base, BA, OPS))

    file_path = 'resource/txt/Pitcher.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        x, y, frame_number, action = 600, 100, 1, 0
        for content in file:
            content = content.strip().split()
            name, strike_out, four_balls, ERA, pitching = content[0], content[1], content[2], content[3], \
                [content[4], content[5], content[6]]
            pitchers.append(Pitcher(x, y, frame_number, action, name, strike_out, four_balls, ERA, pitching))