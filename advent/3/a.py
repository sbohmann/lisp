from io import open
import re
from functools import reduce


def run():
    pieces = []
    for raw_line in open('input.txt'):
        line = raw_line.strip()
        pieces.append(Piece(line))
    width, height = size = calculate_size(pieces)
    print(size)
    solution = Solution(width, height, pieces)
    print(solution.overlaps)
    print(solution.possible_piece)


piece_pattern = re.compile('#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')


class Piece:
    def __init__(self, description):
        match = piece_pattern.fullmatch(description)
        if match is None:
            raise ValueError('Invalid decription [' + description + ']')
        self.id = int(match[1])
        self.x = int(match[2])
        self.y = int(match[3])
        self.width = int(match[4])
        self.height = int(match[5])
        print(self)

    def __str__(self):
        return 'Piece { id: ' + str(self.id) + \
               ', x: ' + str(self.x) + \
               ', y: ' + str(self.y) + \
               ', width: ' + str(self.width) + \
               ', height: ' + str(self.height) + ' }'


def calculate_size(pieces):
    return reduce(adjust_size, pieces, (0, 0))


def adjust_size(size, piece):
    return (
        max(size[0], piece.x + piece.width),
        max(size[1], piece.y + piece.height))


class Solution(object):
    def __init__(self, width, height, pieces):
        self._width = width
        self._height = height
        self._pieces = pieces
        self._calculate()

    def _calculate(self):
        self._create_map()
        self._count_overlaps()
        self._determine_possible_piece()

    def _create_map(self):
        self._map = [0] * (self._width * self._height)
        self._fillMap()

    def _fillMap(self):
        for piece in self._pieces:
            self._adjust_map(piece)

    def _adjust_map(self, piece):
        for y in range(piece.y, piece.y + piece.height):
            for x in range(piece.x, piece.x + piece.width):
                self._increase_field(x, y)

    def _increase_field(self, x, y):
        index = self._field_index(x, y)
        self._map[index] = self._map[index] + 1

    def _field_index(self, x, y):
        if x < 0 or y < 0 or x >= self._width or y >= self._height:
            raise ValueError('Location out of bounds - x: ' + str(x) + ', y: ' + str(y))
        return y * self._width + x

    def _count_overlaps(self):
        self.overlaps = reduce(count_overlaps, self._map, 0)

    def _determine_possible_piece(self):
        self.possible_piece = None
        for piece in self._pieces:
            self._check_piece_for_possibility(piece)

    def _check_piece_for_possibility(self, piece):
        possible = self._determine_possibility(piece)
        if possible:
            if self.possible_piece is not None:
                raise ValueError('Encountered two possible pieces')
            self.possible_piece = piece

    def _determine_possibility(self, piece):
        for y in range(piece.y, piece.y + piece.height):
            for x in range(piece.x, piece.x + piece.width):
                index = self._field_index(x, y)
                count = self._map[index]
                if count < 1:
                    raise ValueError()
                elif count > 1:
                    return False
        return True



def count_overlaps(count, value):
    if value > 1:
        return count + 1
    else:
        return count

run()
