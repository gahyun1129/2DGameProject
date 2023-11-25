import math
import pico2d
class Camera:
    def __init__(self):
        self.x, self.y = 0, 0  # 카메라 위치
        self.scale = 1.0       # 확대/축소 비율

    def apply(self, target_x, target_y):
        # 실제 좌표에 카메라의 위치를 더하고 확대/축소를 적용합니다.
        view_x = target_x - self.x
        view_y = target_y - self.y
        view_x *= self.scale
        view_y *= self.scale
        return view_x, view_y

    def update(self, target_x, target_y):
        # 카메라 위치를 업데이트합니다.
        self.x = target_x
        self.y = target_y

WIDTH, HEIGHT = 800, 600
pico2d.open_canvas(WIDTH, HEIGHT)

camera = Camera()

while True:
    # 게임 업데이트 로직
    player_x, player_y = 400, 300  # 플레이어의 실제 좌표

    # 카메라 업데이트
    camera.update(player_x, player_y)

    # 화면을 지우고 그리기 시작
    pico2d.clear_canvas()

    # 카메라가 적용된 좌표로 플레이어를 그립니다.
    player_image = pico2d.load_image('resource/image/ball.png')  # 예시 이미지 파일명
    view_x, view_y = camera.apply(player_x, player_y)
    player_image.draw(view_x, view_y)

    # 추가적으로 게임에 필요한 다른 그리기 로직을 수행합니다.

    # 화면을 갱신
    pico2d.update_canvas()
