from pico2d import *


class Player:
    def __init__(self, x, y, action, dir, frame_number, name):
        # 위치, 프레임, anim 번호, 왼/오 방향
        self.x, self.y = x, y
        self.frame, self.frame_number, self.action = 0, frame_number, action
        self.dir = dir
        self.name = name

    def handle_events(self, event):
        pass


class Pitcher(Player):
    image = None

    def __init__(self):
        super().__init__()
        if Pitcher.image is None:
            Pitcher.image = load_image('resource/image/character_pitcher.png')

    def render(self):
        Pitcher.image.clip_draw(self.frame*50, 0, 50, 50, self.x, self.y)

    def update(self):
        self.frame = (self.frame + 1) % 8


class Hitter(Player):
    # 클래스 변수, 모든 객체가 하나의 image 나눠 사용.
    image = None

    def __init__(self, x, y, action, dir, frame_number, name, hit, home_run, stolen_base, BA, OPS):
        # 부모의 생성자 물려 받음.
        super().__init__(x, y, action, dir, frame_number, name)

        # 클래스 변수가 설정 == None, 설정 하기.
        if Hitter.image is None:
            Hitter.image = load_image('resource/image/character_hitter.png')

        # 안타, 홈런, 도루, 타율, 출루율 + 장타율
        self.hit, self.home_run, self.stolen_base, self.BA, self.OPS = hit, home_run, stolen_base, BA, OPS

    def render(self):
        Hitter.image.clip_draw(self.frame * 50, self.action, 50, 50, self.x, self.y)

    def update(self):
        self.frame = (self.frame + 1) % self.frame_number