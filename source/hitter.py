from player import Player


class Hitter(Player):
    def __init__(self, x, y, action, dir, frame_number, name, hit, home_run, stolen_base, BA, OPS):
        # 부모의 생성자 물려 받음.
        super().__init__(x, y, action, dir, frame_number, name)

        # 안타, 홈런, 도루, 타율, 출루율 + 장타율
        self.hit, self.home_run, self.stolen_base, self.BA, self.OPS = hit, home_run, stolen_base, BA, OPS

    def draw(self):
        if self.is_draw is True:
            self.image.clip_draw(self.frame * 50, self.action, 50, 50, self.x, self.y)

    def update(self):
        self.frame = (self.frame + 1) % self.frame_number