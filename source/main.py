# 게임의 메인이 되는 코드
# 현재 시작 모드: logo_mode

from pico2d import open_canvas, close_canvas
import game_framework
import mode.logo_mode as start_mode

open_canvas(1000, 1000, sync=True)
game_framework.run(start_mode)
close_canvas()
