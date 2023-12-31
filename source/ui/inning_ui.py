from pico2d import load_image


class InningUI:
    inning_image = None
    number_image = None

    def __init__(self):
        self.frame = 0      # 1 ~ 5
        self.turn = 3  # 3이면 초, 2면 말
        self.goal_x, goal_y = 500, 500
        self.x, self.y = 1000, 500
        self.size = 1
        if InningUI.inning_image is None:
            InningUI.inning_image = load_image('resource/image/UI.png')
            InningUI.number_image = load_image('resource/image/UI.png')

    def update(self):
        if self.x > self.goal_x:
            self.x -= 50
        else:
            self.size = 0.5
            self.x, self.y = 110, 550

    def draw(self):
        self.inning_image.clip_draw(0, self.turn * 50, 250, 50, self.x, self.y, 250 * self.size,
                                    50 * self.size)
        self.number_image.clip_draw((self.frame % 5) * 50, (self.frame // 6) * 50, 50, 50,
                                    self.x - (150 * self.size), self.y - (5 * self.size), 50 * self.size, 50 * self.size)
