class Vehicle:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.turn_state = 0

    def move(self):
        dx, dy = direction_offset[self.direction]
        self.x += dx
        self.y += dy


direction_offset = {
    1: (0, -1),
    2: (1, 0),
    3: (0, 1),
    4: (-1, 0)
}
