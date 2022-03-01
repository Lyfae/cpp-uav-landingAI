def move_x(direction):
    if direction == '+':
        print("Move x+ Mode Detected")
        return bytes('a', 'utf-8')
    if direction == '-':
        print("Move x- Mode Detected")
        return bytes('b', 'utf-8')

def move_y(direction):
    if direction == '+':
        print("Move y+ Mode Detected")
        return bytes('c', 'utf-8')
    if direction == '-':
        print("Move y- Mode Detected")
        return bytes('d', 'utf-8')

def move_z(direction):
    if direction == '+':
        print("Move z+ Mode Detected")
        return bytes('e', 'utf-8')
    if direction == '-':
        print("Move z- Mode Detected")
        return bytes('f', 'utf-8')

def state(mode):
    if mode == 'panic':
        print("Panic Mode Toggle")
        return bytes('y', 'utf-8')
    if mode == 'lock':
        print("Throttle Lock Toggle")
        return bytes('x', 'utf-8')

