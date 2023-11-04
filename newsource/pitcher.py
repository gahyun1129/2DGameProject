from pico2d import load_image


class Pitcher:
    image = None

    def __init__(self, x, y, name, strike_out, four_balls, ERA, pitching):
        # 위치, 현재 프레임, 현재 action, 프레임의 길이
        self.x, self.y = x, y
        self.frame, self.frame_number, self.action = 0, 1, 0

        # 파일: 이름, 탈삼진, 볼넷, ERA, 투구법 2개
        self.name, self.strike_out, self.four_balls, self.ERA, self.pitching = name, strike_out, four_balls, ERA, pitching

        # 이미지 로드
        if Pitcher.image is None:
            Pitcher.image = load_image('resource/image/character_hitter.png')

    def update(self):
        self.frame = (self.frame + 1) % self.frame_number

    def draw(self):
        Pitcher.image.clip_draw(self.frame*50, self.action * 50, 50, 50, self.x, self.y)
