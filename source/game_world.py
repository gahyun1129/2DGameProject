# 게임 월드 관리 모듈
# 게임의 Object 관리

from player import Pitcher, Hitter

hitter_player = []

def init():
    global hitter_player
    file_path = 'resource/txt/Hitter.txt'

    with open(file_path, 'r', encoding='utf-8') as file:
        x, y, action, dir, frame_number = 400, 70, 0, 0, 6
        for content in file:
            content = content.strip().split()
            name, hit, home_run, stolen_base, BA, OPS = content[0], content[1], content[2], content[3], content[4], \
                content[5]
            hitter_player.append(Hitter(x, y, action, dir, frame_number, name, hit, home_run, stolen_base, BA, OPS))