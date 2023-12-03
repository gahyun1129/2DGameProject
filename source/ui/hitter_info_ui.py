from pico2d import load_image, load_font
import server


class HitterInfoUI:
    image = None

    def __init__(self):
        self.font = load_font('resource/txt/DungGeunMo.TTF', 18)
        self.hitter_image = load_image('resource/image/hitter_red.png')
        if HitterInfoUI.image is None:
            HitterInfoUI.image = load_image('resource/image/hitter_info.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(120, 100)
        self.font.draw(130, 115, f'{server.cur_hitter.name}', (0, 0, 0))
        self.font.draw(150, 70, f'{server.cur_hitter.BA}', (0, 0, 0))
        self.hitter_image.draw(70, 100)
