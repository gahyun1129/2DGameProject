from pico2d import load_image, load_font
import server


class GameInfoUI:
    image = None

    def __init__(self):
        self.font = load_font('resource/txt/DungGeunMo.TTF', 24)
        self.hitter_image = load_image('resource/image/hitter_red.png')
        self.out_count_image = load_image('resource/image/out_count.png')
        self.ball_count_image = load_image('resource/image/ball_count.png')
        self.strike_count_image = load_image('resource/image/strike_count.png')

        if GameInfoUI.image is None:
            GameInfoUI.image = load_image('resource/image/game_info.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(150, 530)
        # self.font.draw(130, 115, f'{server.cur_hitter.name}', (0, 0, 0))
        # self.font.draw(150, 70, f'{server.cur_hitter.BA}', (0, 0, 0))
        # self.hitter_image.draw(70, 100)
        self.ball_count_image.clip_draw(server.cur_hitter.ball * 60, 0, 60, 15, 88, 515)
        self.strike_count_image.clip_draw(server.cur_hitter.strike * 40, 0, 40, 15, 95, 500)
        self.out_count_image.clip_draw(server.out_count * 40, 0, 40, 15, 148, 500)

        self.font.draw(260, 560, f'{server.user_score}', (255, 255, 255))
        self.font.draw(260, 530, f'{server.com_score}', (255, 255, 255))
