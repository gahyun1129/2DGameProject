import define
import game_world
class test:
    def __init__(self):
        self.x = 0
    def print_x(self):
        print(self.x)

l = [test() for _ in range(7)]
print(*l[1:5].x)