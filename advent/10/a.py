from io import open
import re


star_pattern = re.compile('position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>')


def run():
    stars = []
    for raw_line in open('input.txt'):
        line = raw_line.strip()
        match = star_pattern.fullmatch(line)
        x, y, vx, vy = map(int, match.groups())
        stars.append(Star(x, y, vx, vy))

    original_stars = list(map(lambda star: star.copy(), stars))

    # maximum_square_sum = 0.0
    # for index in range(0, 100_000):
    #     bounds = calculate_bounds(stars)
    #     field = Field(bounds)
    #     paint_stars(stars, field)
    #     square_sum = calculate_square_sums(stars, field)
    #     if square_sum > maximum_square_sum * 1.1 or index % 100 == 0:
    #         print('index:', index)
    #         print('bounds:', bounds.minx, bounds.miny, bounds.maxx, bounds.maxy, bounds.w, bounds.h)
    #         print('new maximum square_sum:', square_sum)
    #     if square_sum > maximum_square_sum:
    #         maximum_square_sum = square_sum
    #     for star in stars:
    #         star.move()

    for offset in range(-2, 3):
        stars = list(map(lambda star: star.copy(), original_stars))
        for star in stars:
            star.move_n_times(10612 + offset)
        bounds = calculate_bounds(stars)
        display = Display(bounds)
        paint_stars(stars, display)
        for y in range(bounds.miny, bounds.maxy + 1):
            for x in range(bounds.minx, bounds.maxx + 1):
                print('█' if display[x, y] else ' ', sep='', end='')
            print('')




class Star:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def move_n_times(self, n):
        self.x += self.vx * n
        self.y += self.vy * n

    def copy(self):
        return Star(self.x, self.y, self.vx, self.vy)


def calculate_bounds(stars):
    minx = min(stars, key=lambda star: star.x).x
    miny = min(stars, key=lambda star: star.y).y
    maxx = max(stars, key=lambda star: star.x).x
    maxy = max(stars, key=lambda star: star.y).y
    w = maxx - minx + 1
    h = maxy - miny + 1
    return Bounds(minx, miny, maxx, maxy, w, h)


class Bounds:
    def __init__(self, minx, miny, maxx, maxy, w, h):
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy
        self.w = w
        self.h = h


class Field:
    def __init__(self, bounds):
        self._bounds = bounds
        self.rows = [0] * bounds.h
        self.columns = [0] * bounds.w

    def __setitem__(self, coordinates, value):
        x, y = self._relative_coordinates(coordinates)
        row, column = self._calculate_offsets(x, y)
        self.rows[row] += 1
        self.columns[column] += 1

    def _relative_coordinates(self, coordinates):
        abs_x, abs_y = coordinates
        rel_x = abs_x - self._bounds.minx
        rel_y = abs_y - self._bounds.miny
        return rel_x, rel_y

    def _calculate_offsets(self, x, y):
        if x >= 0 and y >= 0 and x < self._bounds.w and y < self._bounds.h:
            return y, x
        else:
            return None


def paint_stars(stars, field):
    for star in stars:
        field[star.x, star.y] = True


def calculate_square_sums(stars, field):
    return calculate_square_sum(field.rows) + calculate_square_sum(field.columns)


def calculate_square_sum(data):
    result = 0
    for value in data:
        result += value * value
    result /= len(data)
    return result


class Display:
    def __init__(self, bounds):
        self._bounds = bounds
        self._data = [False] * (bounds.w * bounds.h)

    def __getitem__(self, coordinates):
        x, y = self._relative_coordinates(coordinates)
        offset = self._calculate_offset(x, y)
        return self._data[offset] if offset else False

    def __setitem__(self, coordinates, value):
        x, y = self._relative_coordinates(coordinates)
        offset = self._calculate_offset(x, y)
        self._data[offset] = value

    def _relative_coordinates(self, coordinates):
        abs_x, abs_y = coordinates
        rel_x = abs_x - self._bounds.minx
        rel_y = abs_y - self._bounds.miny
        return rel_x, rel_y

    def _calculate_offset(self, x, y):
        if x >= 0 and y >= 0 and x < self._bounds.w and y < self._bounds.h:
            return y * self._bounds.w + x
        else:
            return None


run()
