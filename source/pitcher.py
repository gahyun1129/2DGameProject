from player import Player


class Pitcher(Player):
    def __init__(self, x, y, action, dir, frame_number, name, strike_out, four_balls, ERA, pitching):
        # 부모의 생성자 물려 받음.
        super().__init__(x, y, action, dir, frame_number, name)

        # 탈삼진, 볼넷, ERA, 투구법 2개
        self.strike_out, self.four_balls, self.ERA, self.pitching = strike_out, four_balls, ERA, pitching

    def draw(self):
        if self.is_draw is True:
            self.image.clip_draw(self.frame*50, self.action, 50, 50, self.x, self.y)

    def update(self):
        self.frame = (self.frame + 1) % self.frame_number