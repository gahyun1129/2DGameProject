from define import *
from pico2d import load_image
import random

class Ball:
    image = None

    def __init__(self):
        # 위치, 현재 프레임, 프레임의 길이
        self.pos = mound
        self.frame, self.frame_number = 0, 1
        self.current_pos = mound
        self.goal_pos = home
        self.t = 0.0

        # 이미지 로드
        if Ball.image is None:
            Ball.image = load_image('resource/image/ball.png')

        # 상태머신 추가
        # self.state_machine = None
        # self.state_machine.start()

    def update(self):
        self.frame = (self.frame + 1) % self.frame_number
        if self.t < 1.0:
            self.frame = (self.frame + 1) % self.frame_number
            x = (1 - self.t) * self.current_pos[0] + self.t * self.goal_pos[0]
            y = (1 - self.t) * self.current_pos[1] + self.t * self.goal_pos[1]
            self.pos = (x, y)
            self.t += 0.1
        else:
            self.pos = self.goal_pos

    def draw(self):
        Ball.image.clip_draw(self.frame * 50, 0, 50, 50, self.pos[0], self.pos[1], 20, 20)

    def hit_success(self):
        self.current_pos = home
        x = random.randint(50, 750)
        y = random.randint(300, 500)
        self.goal_pos = (x, y)
        self.t = 0.0

    def hit_fail(self):
        pass
