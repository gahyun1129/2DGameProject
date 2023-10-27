class Player:
    def __init__(self):
        self.x, self.y = 400, 60
        self.frame = 0
        self.action = 3
        self.dir = 0

    def update(self):
        pass

    def handle_events(self):
        pass

    def render(self):
        pass


class Pitcher(Player):
    image = None

    def __int__(self):
        super.__init__()
        if image == None:
            image = load_image('resource/image/character_pitcher.png')
