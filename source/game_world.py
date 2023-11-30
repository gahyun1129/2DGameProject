import server

# objects[0] : 배경, ball
# objects[1] : 수비수
# objects[2] : 주자 및 타자
# objects[3] : UI

objects = [[], [], [], [], []]

collision_pairs = {}


## 렌더링 오브젝트(objects) 관리 ##
def add_object(o, depth=0):
    objects[depth].append(o)


def add_objects(ol, depth=0):
    objects[depth] += ol


def update():
    for layer in objects:
        for o in layer:
            o.update()


def render():
    for layer in objects:
        for o in layer:
            o.draw()


def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            del o
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in objects:
        layer.clear()


## 충돌 오브젝트(collision_pairs) 관리 ##
def collide(a, b):
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ta < bb: return False
    if ba > tb: return False

    return True


def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[], []]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)


def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)


def clear_collision_pairs():
    collision_pairs.clear()


def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)


## 그 외의 오브젝트 관리 ##
def update_handle_event(event):
    # 공
    server.ball.state_machine.handle_event(event)

    # 주자
    for o in objects[2]:
        o.state_machine.handle_event(event)

    # 수비수 (투수, 포수 제외)
    for o in objects[1][2:9]:
        if o.run_to_ball(server.ball.goal_position):
            o.state_machine.handle_event(event)


