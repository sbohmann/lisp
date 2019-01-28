from io import open
import re
from functools import reduce

pattern = re.compile('(\d+), (\d+)')

def run():
    points = []
    id = 1
    for rawline in open('input.txt'):
        line = rawline.strip()
        match = pattern.fullmatch(line)
        if match is None:
            raise ValueError(line)
        points.append(Point(id, int(match[1]), int(match[2])))
        id += 1

    for point in points:
        print(point)

    minx = min(points, key=lambda point: point.x).x
    miny = min(points, key=lambda point: point.y).y
    maxx = max(points, key=lambda point: point.x).x
    maxy = max(points, key=lambda point: point.y).y
    print(minx, miny, maxx, maxy)

    width = maxx - minx + 1
    height = maxy - miny + 1

    field = Field(minx, miny, width, height)

    disqualified_points = set()
    frequencies = {}
    points_with_low_distance_sum = 0

    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            closest_point = min(points, key=lambda point: distance(x, y, point.x, point.y))
            if x == 0 or y == 0 or x == maxx or y == maxy:
                disqualified_points.add(closest_point.id)
            field[x, y] = closest_point
            frequency = frequencies.get(closest_point.id, 0)
            frequencies[closest_point.id] = frequency + 1
            distance_sum = reduce(lambda sum, point: sum + distance(x, y, point.x, point.y), points, 0)
            if distance_sum < 10_000:
                points_with_low_distance_sum += 1

    relevant_points = filter(lambda item: item[0] not in disqualified_points, frequencies.items())
    most_frequent_relevant_point = max(relevant_points, key=lambda item: item[1])
    print('most frequent relevant point:', most_frequent_relevant_point)
    print('points_with_low_distance_sum:', points_with_low_distance_sum)


class Point:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return 'Point(x: ' + str(self.x) + ', y: ' + str(self.y) + ')'


class Field:
    def __init__(self, startx, starty, width, height):
        self.startx = startx
        self.starty = starty
        self.width = width
        self.height = height
        self.data = [None] * width * height

    def __getitem__(self, coordinates):
        x, y = coordinates
        self._check_bounds(x, y)
        return self.data[(y - self.starty) * self.width + (x - self.startx)]

    def __setitem__(self, coordinates, value):
        x, y = coordinates
        self._check_bounds(x, y)
        self.data[(y - self.starty) * self.width + (x - self.startx)] = value

    def _check_bounds(self, x, y):
        if x < self.startx or y < self.starty or x >= self.startx + self.width or y >= self.starty + self.height:
            raise ValueError('Out of bounds: [' + str(x) + ', ' + str(y) + ']')


def distance(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)


run()
