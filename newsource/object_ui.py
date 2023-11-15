from pico2d import load_image, load_font


class UI:
    image = None
    image_bar = None

    def __init__(self):
        self.font = load_font('resource/txt/NanumGothic.TTF', 16)
        if UI.image is None:
            UI.image = load_image('resource/image/UI.png')
        if UI.image_bar is None:
            UI.image_bar = load_image('resource/image/UI_bar.png')

    def update(self):
        pass

    def draw(self):
        # rect = to_sdl_rect(x-w/2, y-h/2, w, h)
        self.image_bar.draw(400 - 50, 50, 100, 50)

    def draw_with_ment(self, ment):
        self.image.draw(400, 50, 100, 50)
        self.font.draw(390, 50, f'{ment}', (0, 0, 255))
