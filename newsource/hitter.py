from pico2d import load_image


class Hitter:
    image = None

    def __init__(self, x, y, frame_number, action, team_color, name, hit, home_run, stolen_base, BA, OPS):
        # 위치, 현재 프레임, 현재 action, 프레임의 길이, 팀 색 결정
        self.x, self.y = x, y
        self.frame, self.frame_number, self.action = 0, frame_number, (action + team_color)
        # self.team_color = team_color

        # 파일: 이름, 안타, 홈런, 도루, 타율, 출루율 + 장타율
        self.name, self.hit, self.home_run, self.stolen_base, self.BA, self.OPS = name, hit, home_run, stolen_base, BA, OPS

        # 이미지 로드
        if Hitter.image is None:
            Hitter.image = load_image('resource/image/character_hitter.png')

    def update(self):
        self.frame = (self.frame + 1) % self.frame_number

    def draw(self):
        Hitter.image.clip_draw(self.frame * 50, self.action * 50, 50, 50, self.x, self.y)
