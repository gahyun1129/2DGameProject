import attack_mode

objects = [[], [], [], []]


def add_object(o, depth=0):
    objects[depth].append(o)


def add_objects(ol, depth=0):
    objects[depth] += ol


def add_layer(ol):
    objects.append(ol)


def update():
    for layer in objects:
        for o in layer:
            o.update()


def render():
    for layer in objects:
        for o in layer:
            o.draw()


def update_handle_event(event):
    # 주자
    for o in objects[2]:
        o.state_machine.handle_event(event)

    # 수비수 (투수 제외)
    for o in objects[1][1:9]:
        if o.run_to_ball(attack_mode.ball.goal_position):
            o.state_machine.handle_event(event)


def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            del o
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in objects:
        layer.clear()  # layer type은 list이므로
