import attack_mode

objects = [[]]


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


def update_handle_event():
    if attack_mode.current_event[0] == 'HIT_SUCCESS':
        for o in objects[2]:
            o.state_machine.handle_event(('HIT_SUCCESS', 0))


def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in objects:
        layer.clear()           # layer type은 list이므로