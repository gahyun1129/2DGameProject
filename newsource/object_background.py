from pico2d import *


class Background:
    def __init__(self):
        self.image = load_image('resource/image/background.png')
        self.cw = get_canvas_width()
        self.ch = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h
        print(self.w, self.h)
        print(self.cw, self.ch)

    def update(self):
        self.window_left = clamp(0, (self.w - self.cw) // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, (self.h - self.ch) // 2, self.h - self.ch - 1)

    def draw(self):
        # self.image.clip_draw_to_origin(100, 0, self.cw // 2, self.ch // 2, 0, 0)
        w, h = self.cw, self.ch
        size = 2
        self.image.clip_draw_to_origin(200*size, 50, w, h, 0, 0, w * size, h * size)
        # self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)
