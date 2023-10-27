from pico2d import *


running = True
open_canvas()
grass = load_image('resource/image/grass.png')
character = load_image('resource/image/idle.png')
frame = 0

while running:
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(frame * 50, 0, 50, 50, 400, 70)
    frame = (frame+1) % 4
    update_canvas()
    delay(0.5)

close_canvas()