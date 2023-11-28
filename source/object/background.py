from pico2d import *


class Background:
    def __init__(self):
        self.image = load_image('resource/image/background.png')

        self.cw = get_canvas_width()
        self.ch = get_canvas_height()

        self.w = self.image.w
        self.h = self.image.h

        self.window_left = (self.image.w - self.cw) // 2
        self.window_bottom = 0

    def update(self):
        # ball의 위치에 연동되어 위치 스크롤링 될 것!!
        pass
        # self.window_left = clamp(0, (self.w - self.cw) // 2, self.w - self.cw - 1)
        # self.window_bottom = clamp(0, (self.h - self.ch) // 2, self.h - self.ch - 1)

    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)
