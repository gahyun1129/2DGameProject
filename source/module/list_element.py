from pico2d import load_image, load_font, draw_rectangle
import server


class Element:
    image = None

    def __init__(self, position, player):
        self.font = load_font('resource/txt/DungGeunMo.TTF', 16)

        self.is_selected = False  # true면 1 false면 0
        self.x, self.y = 0, 0
        self.position = position
        self.player = player

        if Element.image is None:
            Element.image = load_image('resource/image/player_list.png')

    def get_bb(self):
        return self.x - 180, self.y - 45, self.x + 180, self.y + 45

    def set_x_y(self, x, y):
        self.x, self.y = x, y

    def handle_collide(self):
        if self.position == '투수':
            if self.is_selected:
                self.is_selected = False
                server.select_pitcher_num = 0
                server.selected_pitcher = None
            else:
                if server.select_pitcher_num != 1:
                    self.is_selected = True
                    server.select_pitcher_num = 1
                    server.selected_pitcher = self.player
        else:
            if self.is_selected:
                self.is_selected = False
                server.select_hitter_num -= 1
                server.selected_hitter.remove(self.player)
            else:
                if server.select_hitter_num < 9:
                    self.is_selected = True
                    server.select_hitter_num += 1
                    server.selected_hitter.append(self.player)

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(int(self.is_selected) * 360, 0, 360, 90, self.x, self.y)
        draw_rectangle(*self.get_bb())
        if self.position == '투수':
            self.font.draw(self.x - 170, self.y + 20, f'이름: {self.player.name}', (0, 0, 0))
        else:
            self.font.draw(self.x - 170, self.y + 20, f'이름: {self.player.name}', (255, 0, 0))
