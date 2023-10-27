from pico2d import *


running = True
open_canvas()
grass = load_image('resource/image/grass.png')

while running:
    clear_canvas()
    grass.draw(400, 30)
    update_canvas()

close_canvas()