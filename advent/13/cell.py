class Cell:
    def __init__(self):
        self._horizontal = False
        self._vertical = False
        self._slash = False
        self._backslash = False

    def horizontal(self):
        self._horizontal = True
        return self

    def vertical(self):
        self._vertical = True
        return self

    def slash(self):
        self._slash = True
        return self

    def backslash(self):
        self._backslash = True
        return self

    # 1 up, 2 right, 3 down, 4 left
    def change_vehicle_direction(self, vehicle):
        if self._horizontal and self._vertical:
            self._rotate_vehicle_according_to_state(vehicle)
        elif vehicle.direction == 1:
            if self._slash:
                vehicle.direction = 2
            elif self._backslash:
                vehicle.direction = 4
        elif vehicle.direction == 2:
            if self._slash:
                vehicle.direction = 1
            elif self._backslash:
                vehicle.direction = 3
        elif vehicle.direction == 3:
            if self._slash:
                vehicle.direction = 4
            elif self._backslash:
                vehicle.direction = 2
        elif vehicle.direction == 4:
            if self._slash:
                vehicle.direction = 3
            elif self._backslash:
                vehicle.direction = 1
        else:
            raise ValueError()

    def _rotate_vehicle_according_to_state(self, vehicle):
        offset = 0
        if vehicle.turn_state == 0:
            offset = 3
        elif vehicle.turn_state == 2:
            offset = 1
        vehicle.direction = (vehicle.direction - 1 + offset) % 4 + 1
        vehicle.turn_state = (vehicle.turn_state + 1) % 3
