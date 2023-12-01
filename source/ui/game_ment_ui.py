from pico2d import load_image

import server


class MentUI:
    ment_image = None
    number_image = None

    def __init__(self):
        self.frame = 0      # 1 ~ 5
        self.ment = 6       # 6: ball, 7: strike, 8: hit
        self.x, self.y = 600, 200

        self.is_draw_number = False
        self.is_draw = False

        if MentUI.ment_image is None:
            MentUI.ment_image = load_image('resource/image/UI.png')
            MentUI.number_image = load_image('resource/image/UI.png')

    def update(self):
        pass

    def draw(self):
        if self.is_draw:
            self.ment_image.clip_draw(0, self.ment * 50, 250, 50, self.x, self.y)
            if self.is_draw_number:
                self.number_image.clip_draw(self.frame * 50, 0, 50, 50, self.x - 80, self.y - 2)

    def draw_ment_ui(self, status, number=0):
        if status == 'strike':
            self.is_draw, self.is_draw_number = True, True
            self.frame = number
            self.ment = 7
        elif status == 'ball':
            self.is_draw, self.is_draw_number = True, True
            self.frame = number
            self.ment = 6
        elif status == 'hit':
            self.is_draw, self.is_draw_number = True, False
            self.ment = 8
