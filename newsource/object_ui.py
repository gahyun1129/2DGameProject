from pico2d import load_image, load_font


class UI:
    image = None
    image_bar = None

    def __init__(self):
        self.font = load_font('resource/txt/NanumGothic.TTF', 16)
        self.frame = 0
        self.action = 0
        self.is_update = True
        if UI.image is None:
            UI.image = load_image('resource/image/progress_bar.png')

    def update(self):
        if self.is_update:
            self.frame = (self.frame + 1) % 4
            if self.frame == 0:
                self.action = (self.action + 1) % 5

    def draw(self):
        # rect = to_sdl_rect(x-w/2, y-h/2, w, h)
        self.image.clip_draw(self.frame * 300, self.action * 50, 300, 50, 400, 50)

    def draw_with_ment(self, ment):
        self.image.draw(400, 50, 100, 50)
        self.font.draw(390, 50, f'{ment}', (0, 0, 255))
