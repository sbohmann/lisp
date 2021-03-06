offsets = [(0, -1), (-1, 0), (1, 0), (0, 1)]


def add(position, offset):
    x, y = position
    dx, dy = offset
    return x + dx, y + dy


# TODO add optional stop criterion function parameter and give access to number of last round if stopped
class FloodSearch:
    def __init__(self, situation, starting_position):
        self._situation = situation
        self._positions = {starting_position}
        self._distances = self._build_distances(situation)
        self[starting_position] = 0
        self._calculate_distances()

    def _build_distances(self, situation):
        return [[None] * situation.width for _ in range(situation.height)]

    def __getitem__(self, coordinates):
        x, y = coordinates
        self._situation.check_range(x, y)
        return self._distances[y][x]

    def __setitem__(self, coordinates, new_distance):
        x, y = coordinates
        self._situation.check_range(x, y)
        self._distances[y][x] = new_distance

    def _calculate_distances(self):
        while self._positions:
            workload = self._positions
            self._positions = set()
            for position in workload:
                self._calculate_distances_for_position(position)

    def _calculate_distances_for_position(self, position):
        for offset in offsets:
            neighbor = add(position, offset)
            if self._situation.free(*neighbor):
                self._update_distance_and_add_position(neighbor, self[position] + 1)

    def _update_distance_and_add_position(self, neighbor, new_distance):
        if self._update_distance(neighbor, new_distance):
            self._positions.add(neighbor)

    def _update_distance(self, coordinates, new_distance):
        current_distance = self[coordinates]
        if current_distance is None or new_distance < current_distance:
            self[coordinates] = new_distance
            return True
        else:
            return False
