from pico2d import *


class Grass:
    def __init__(self):
        self.image = load_image('resource/image/background.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(600, 450)
