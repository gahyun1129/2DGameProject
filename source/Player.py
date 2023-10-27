class Palyer:
    def __init__(self):
        self.x, self.y = 400, 60
        self.frame = 0
        self.action = 3
        self.dir = 0
        self.face_dir = 1
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()

    def fire_ball(self):
        ball = Ball(self.x, self.y, self.face_dir*10)
        game_world.add_object(ball, 1)