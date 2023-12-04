from pico2d import *
import server

class Background:
    def __init__(self):
        self.image = load_image('resource/image/background.png')

        self.cw = get_canvas_width()
        self.ch = get_canvas_height()

        self.w = self.image.w
        self.h = self.image.h

        self.window_left = (self.image.w - self.cw) // 2
        self.window_bottom = 0

        # self.bgm = load_music('resource/sound/background.mp3')
        # self.bgm.set_volume(32)
        # self.bgm.repeat_play()

    def update(self):
        self.window_left = int(server.ball.pos[0]) - self.cw // 2
        self.window_bottom = int(server.ball.pos[1]) - self.ch // 2

        self.window_left = clamp(0, self.window_left, self.w - self.cw - 1)
        self.window_bottom = clamp(0, self.window_bottom, self.h - self.ch - 1)
        pass
    def draw(self):
        self.image.clip_draw_to_origin(self.window_left, self.window_bottom, self.cw, self.ch, 0, 0)
