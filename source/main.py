from pico2d import *


running = True
open_canvas()
grass = load_image('resource/image/grass.png')
character = load_image('resource/image/character_hitter.png')
character2 = load_image('resource/image/character_pitcher.png')
frame = 0
frame2 = 0

while running:
    clear_canvas()
    grass.draw(400, 30)
    character.clip_draw(frame * 50, 0, 50, 50, 200, 70)
    character2.clip_draw(frame * 50, 0, 50, 50, 600, 70)
    frame = (frame+1) % 6
    frame2 = (frame+1) % 8
    update_canvas()
    delay(0.2)

close_canvas()