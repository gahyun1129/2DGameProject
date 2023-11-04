from pico2d import *
class Player:
    image = None
    def __init__(self, x, y, action, dir, frame_number, name):
        # 위치, 프레임, anim 번호, 왼/오 방향
        self.x, self.y = x, y
        self.frame, self.frame_number, self.action = 0, frame_number, action
        self.dir = dir
        self.name = name
        if Player.image is None:
            Player.image = load_image('resource/image/character_hitter.png')

class Pitcher(Player):
    def __init__(self, x, y, action, dir, frame_number, name, strike_out, four_balls, ERA, pitching):
        # 부모의 생성자 물려 받음.
        super().__init__(x, y, action, dir, frame_number, name)

        # 탈삼진, 볼넷, ERA, 투구법 2개
        self.strike_out, self.four_balls, self.ERA, self.pitching = strike_out, four_balls, ERA, pitching

    def draw(self):
        self.image.clip_draw(self.frame*50, self.action, 50, 50, self.x, self.y)

    def update(self):
        self.frame = (self.frame + 1) % self.frame_number

open_canvas()
p = Pitcher(600, 70, 0, 0, 1, '이름', 3, 2, 1, ['아','이','오'])
imag = load_image('resource/image/character_hitter.png')
p.image.draw_now(p.x, p.y, 50, 300)
delay(5)
close_canvas()
