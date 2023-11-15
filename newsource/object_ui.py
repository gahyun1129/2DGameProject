from pico2d import load_image, load_font


class UI:
    image = None

    def __init__(self):
        if UI.image is None:
            UI.image = load_image('resource/image/UI.png')
            self.font = load_font('resource/txt/NanumGothic.TTF', 16)

    def update(self):
        pass

    def draw(self, ment):
        self.image.draw(400, 50, 100, 50)
        self.font.draw(390, 50, f'{ment}', (0, 0, 255))