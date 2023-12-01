from pico2d import load_image


class JudgeUI:
    judge_image = None
    number_image = None

    def __init__(self):
        self.frame = 0      # 1 ~ 5
        self.judge = 4       # 4: safe, 5: out
        self.x, self.y = 600, 400

        self.is_draw_number = False
        self.is_draw = False

        if JudgeUI.judge_image is None:
            JudgeUI.judge_image = load_image('resource/image/UI.png')
            JudgeUI.number_image = load_image('resource/image/UI.png')

    def update(self):
        pass

    def draw(self):
        if self.is_draw:
            self.judge_image.clip_draw(0, self.judge * 50, 250, 50, self.x, self.y)
            if self.is_draw_number:
                self.number_image.clip_draw(self.frame * 50, 0, 50, 50, self.x - 80, self.y - 2)

    def draw_judge_ui(self, status, number=0):
        if status == 'out':
            self.is_draw, self.is_draw_number = True, True
            self.frame = number
            self.judge = 5
        elif status == 'safe':
            self.is_draw, self.is_draw_number = True, False
            self.judge = 4
