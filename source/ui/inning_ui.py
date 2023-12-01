from pico2d import load_image

import server


class INNINGUI:
    inning_image = None
    number_image = None

    def __init__(self):
        self.frame = 0      # 1 ~ 5
        self.action = 0     # 6 ~ 9
        self.turn = 3  # 3이면 초, 2면 말
        self.goal_x, goal_y = 600, 500
        self.x, self.y = 1300, 500
        self.size = 1
        if INNINGUI.inning_image is None:
            INNINGUI.inning_image = load_image('resource/image/UI.png')
            INNINGUI.number_image = load_image('resource/image/UI.png')

    def update(self):
        if self.x > self.goal_x:
            self.x -= 50
        else:
            self.size = 0.5
            self.x, self.y = 200, 900

    def draw(self):
        self.inning_image.clip_draw(0, self.turn * 100, 500, 100, self.x, self.y, 500 * self.size,
                                    100 * self.size)
        self.number_image.clip_draw(self.frame * 100, self.action * 100, 100, 100,
                                    self.x - (300 * self.size), self.y - (10 * self.size), 100 * self.size, 100 * self.size)
