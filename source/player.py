from pico2d import *
from define import *

class Player:
    def __init__(self, x, y, action, dir, frame_number, name):
        # 위치, 프레임, anim 번호, 왼/오 방향
        self.x, self.y = x, y
        self.frame, self.frame_number, self.action = 0, frame_number, action
        self.dir = dir
        self.name = name
        self.is_draw = True

    def handle_events(self, event):
        pass


class Pitcher(Player):
    image = None

    def __init__(self, x, y, action, dir, frame_number, name, strike_out, four_balls, ERA, pitching):
        # 부모의 생성자 물려 받음.
        super().__init__(x, y, action, dir, frame_number, name)

        # 클래스 변수가 설정 == None, 설정 하기.
        if Pitcher.image is None:
            Pitcher.image = load_image('resource/image/character_pitcher.png')

        # 탈삼진, 볼넷, ERA, 투구법 2개
        self.strike_out, self.four_balls, self.ERA, self.pitching = strike_out, four_balls, ERA, pitching

    def draw(self):
        Pitcher.image.clip_draw(self.frame*50, self.action, 50, 50, self.x, self.y)

    def update(self):
        self.frame = (self.frame + 1) % self.frame_number


class Hitter(Player):
    # 클래스 변수, 모든 객체가 하나의 image 나눠 사용.
    image = None

    def __init__(self, x, y, action, dir, frame_number, name, hit, home_run, stolen_base, BA, OPS):
        # 부모의 생성자 물려 받음.
        super().__init__(x, y, action, dir, frame_number, name)

        # 클래스 변수가 설정 == None, 설정 하기.
        if Hitter.image is None:
            Hitter.image = load_image('resource/image/character_hitter.png')

        # 안타, 홈런, 도루, 타율, 출루율 + 장타율
        self.hit, self.home_run, self.stolen_base, self.BA, self.OPS = hit, home_run, stolen_base, BA, OPS

    def draw(self):
        Hitter.image.clip_draw(self.frame * 50, self.action, 50, 50, self.x, self.y)

    def update(self):
        self.frame = (self.frame + 1) % self.frame_number


def defence_position(players):
    (players[0].x, players[0].y) = mound
    (players[1].x, players[1].y) = one_base
    (players[2].x, players[2].y) = (two_base[0] + 70, two_base[1] - 20)
    (players[3].x, players[3].y) = three_base
    (players[4].x, players[4].y) = home
    (players[5].x, players[5].y) = short
    (players[6].x, players[6].y) = left
    (players[7].x, players[7].y) = right
    (players[8].x, players[8].y) = center
    players[9].is_draw = False


def attack_position(players):
    players[0].is_draw = False
    (players[1].x, players[1].y) = attack_zone
    for i in range(2, 10):
        players[i].is_draw = False