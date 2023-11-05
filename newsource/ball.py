from define import *
from pico2d import load_image


class Ball:
    image = None

    def __init__(self):
        # 위치, 현재 프레임, 프레임의 길이
        self.pos = mound
        self.frame, self.frame_number = 0, 1

        # 이미지 로드
        if Ball.image is None:
            Ball.image = load_image('resource/image/ball.png')

        # 상태머신 추가
        self.state_machine = None
        self.state_machine.start()
