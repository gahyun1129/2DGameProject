from pico2d import *
from define import *
import attack_mode

class Player:
    def __init__(self, x, y, action, dir, frame_number, name):
        # 위치, 프레임, anim 번호, 왼/오 방향
        self.x, self.y = x, y
        self.frame, self.frame_number, self.action = 0, frame_number, action
        self.dir = dir
        self.name = name

    def set_image(self, image_path):
        self.image = load_image(image_path)


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


def attack_position(p):
    attack_mode.cur_hitter = p[1]
    (p[1].x, p[1].y) = attack_zone
