from pico2d import load_image
from sdl2 import SDL_KEYDOWN, SDLK_SPACE

import attack_mode
import game_world
from ball import Ball


# ## 이벤트 체크 함수 ##
# def space_down(e):
#     return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE
#
#
# ## 상태 머신 ##
# class StateMachineHit:
#     def __init__(self, pitcher):
#         self.pitcher = pitcher
#         self.cur_state = Idle
#         self.transitions = {
#             Hit: {hit_success: Run, hit_fail: Idle, hit_done: Idle},
#             Idle: {space_down: Hit},
#             Run: {run_done: Idle}
#         }
#
#     def handle_event(self, e):
#         for check_event, next_state in self.transitions[self.cur_state].items():
#             if check_event(e):
#                 self.cur_state.exit(self.pitcher, e)
#                 self.cur_state = next_state
#                 self.cur_state.enter(self.pitcher, e)
#                 return True
#         return False
#
#     def start(self):
#         self.cur_state.enter(self.pitcher, ('START', 0))
#
#     def update(self):
#         self.cur_state.do(self.pitcher)
#
#     def draw(self):
#         self.cur_state.draw(self.pitcher)


## 클래스 ##
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

        # self.ball = Ball()

    def init_state_machine(self):
        pass

    def update(self):
        self.frame = (self.frame + 1) % self.frame_number
        # if space_down(attack_mode.current_event):
        #     game_world.add_layer([self.ball])

    def draw(self):
        Pitcher.image.clip_draw(self.frame * 50, self.action * 50, 50, 50, self.x, self.y)
