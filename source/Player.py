from pico2d import *


class Player:
    def __init__(self):
        self.x, self.y = 400, 60
        self.frame = 0
        self.action = 0
        self.dir = 0



    def handle_events(self, event):
        pass



class Pitcher(Player):
    image = None

    def __init__(self):
        super().__init__()
        if Pitcher.image == None:
            Pitcher.image = load_image('resource/image/character_pitcher.png')
    def render(self):
        Pitcher.image.clip_draw(self.frame*50, 0, 50, 50, self.x, self.y)
    def update(self):
        self.frame = (self.frame + 1) % 8