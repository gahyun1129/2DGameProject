from pico2d import load_image, load_font
import server

class Element:
    image = None

    def __init__(self, position, player):
        self.font = load_font('resource/txt/DungGeunMo.TTF', 16)

        self.is_selected = False         # true면 1 false면 0
        self.x, self.y = 0, 0
        self.position = position
        self.player = player

        if Element.image is None:
            Element.image = load_image('resource/image/player_list.png')

    def set_x_y(self, x, y):
        self.x, self.y = x, y

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(int(self.is_selected) * 360, 0, 360, 90, self.x, self.y)
        if self.position == '투수':
            self.font.draw(40, self.y + 20, f'이름: {self.player.name}', (0, 0, 0))
        else:
            self.font.draw(260, 560, f'{2}', (255, 255, 255))
