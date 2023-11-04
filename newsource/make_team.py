from hitter import Hitter
from pitcher import Pitcher

hitters = []
pitchers = []


def make_team():
    pass


def set_player_from_data_file():
    file_path = 'resource/txt/Hitter.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        x, y, frame_number, action, team_color = 300, 100, 1, 4, 0
        for content in file:
            content = content.strip().split()
            name, hit, home_run, stolen_base, BA, OPS = content[0], content[1], content[2], content[3], content[4], \
                content[5]
            hitters.append(Hitter(x, y, frame_number, action, team_color, name, hit, home_run, stolen_base, BA, OPS))

    file_path = 'resource/txt/Pitcher.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        x, y, frame_number, action, team_color = 600, 100, 1, 0, 0
        for content in file:
            content = content.strip().split()
            name, strike_out, four_balls, ERA, pitching = content[0], content[1], content[2], content[3], \
                [content[4], content[5], content[6]]
            pitchers.append(Pitcher(x, y, frame_number, action, team_color, name, strike_out, four_balls, ERA, pitching))