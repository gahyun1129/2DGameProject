from pico2d import load_image

import server


class UI:
    image = None

    def __init__(self):
        self.frame = 0
        self.action = 0
        self.is_hit = False
        if UI.image is None:
            UI.image = load_image('resource/image/progress_bar.png')

    def update(self):
        if not self.is_hit:
            self.frame = self.frame + 1
            if self.frame == 5:
                self.action = (self.action + 1) % 5
                self.frame = 0

    def draw(self):
        self.image.clip_draw(self.frame * 600, self.action * 50, 600, 50, 400, 50)
