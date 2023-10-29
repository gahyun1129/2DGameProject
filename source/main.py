from pico2d import *
from player import Pitcher, Hitter


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        # else:
            # pitcher.handle_events(event)


def create_world():
    global running
    global hitter
    global pitcher

    running = True

    # pitcher = Pitcher()
    # hitter = Hitter(400, 70, 0, 0, 6, 0, 0, 0, 0, 0, 0)

    file_path = 'resource/txt/Hitter.txt'

    hitter_player = []

    with open(file_path, 'r', encoding='utf-8') as file:
        x, y, action, dir, frame_number = 400, 70, 0, 0, 6
        for content in file:
            content = content.strip().split()
            name, hit, home_run, stolen_base, BA, OPS = content[0], content[1], content[2], content[3], content[4], \
            content[5]
            hitter_player.append(Hitter(x, y, action, dir, frame_number, name, hit, home_run, stolen_base, BA, OPS))

    hitter = hitter_player[0]


def update_world():
    # pitcher.update()
    hitter.update()


def render_world():
    clear_canvas()
    # pitcher.render()
    hitter.render()
    update_canvas()


open_canvas()
create_world()


# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.2)
# finalization code
close_canvas()