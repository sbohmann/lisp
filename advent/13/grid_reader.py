from grid import Grid
from cell import Cell
from vehicle import Vehicle


class GridReader:
    def __init__(self):
        self._width = None
        self._height = None
        self._rail_map = []
        self._vehicles = []
        self._vehicle_map = []
        self._read_rows()
        self._create_result()

    def _read_rows(self):
        for y, raw_line in enumerate(open('input.txt')):
            line = raw_line.strip('\n')
            self._read_row(line)
            self._read_vehicle_row(line, y)
        self._height = len(self._rail_map)

    def _read_row(self, line):
        row = list(map(interpret_char, line))
        self._set_width(row)
        self._rail_map.append(row)
        self._vehicle_map.append([None] * len(row))

    def _set_width(self, row):
        if self._width is None:
            self._width = len(row)
        elif len(row) != self._width:
            raise ValueError('len(row): ' + str(len(row)) + ', self._width: ' + str(self._width))

    def _read_vehicle_row(self, line, y):
        for x, c in enumerate(line):
            direction = vehicle_direction(c)
            if direction is not None:
                self._vehicles.append(Vehicle(x, y, direction))

    def _create_result(self):
        self.result = Grid(
            self._rail_map,
            self._vehicles,
            self._vehicle_map)


def interpret_char(c):
    return grid_interpretation_table[c]


grid_interpretation_table = {
    ' ': Cell(),
    '-': Cell().horizontal(),
    '<': Cell().horizontal(),
    '>': Cell().horizontal(),
    '|': Cell().vertical(),
    '^': Cell().vertical(),
    'v': Cell().vertical(),
    '+': Cell().horizontal().vertical(),
    '/': Cell().slash(),
    '\\': Cell().backslash()
}


def vehicle_direction(c):
    return vehicle_creation_table.get(c, None)


vehicle_creation_table = {
    '^': 1,
    '>': 2,
    'v': 3,
    '<': 4
}
