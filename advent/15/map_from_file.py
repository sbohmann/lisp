from io import open
import re

from map import Map


line_pattern = re.compile('[#.EG]+')


def _check_line(line):
    if not line_pattern.fullmatch(line):
        raise ValueError('Illegal line [' + str(line) + ']')


def normalize(width):
    return lambda line: list(pad_line(line, width))


def pad_line(line, width):
    return line + ('#' * (width - len(line)))


class MapFromFile:
    def __init__(self, path):
        self._width = 0
        self._height = 0
        self._lines = []
        self.result = None

        self._file = open(path, 'r')
        self._read_lines()
        self._normalize_lines()
        self._create_result()

    def _read_lines(self):
        for raw_line in self._file:
            line = raw_line.strip()
            _check_line(line)
            self._width = max(self._width, len(line))
            self._height += 1
            self._lines.append(line)

    def _normalize_lines(self):
        self._lines = list(map(normalize(self._width), self._lines))

    def _create_result(self):
        self.result = Map(self._width, self._height, self._lines)
