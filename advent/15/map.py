class Map:
    def __init__(self, width, height, lines):
        self.width = width
        self.height = height
        self._lines = lines
        self._check()

    def __getitem__(self, coordinates):
        x, y = coordinates
        self.check_range(x, y)
        return self._lines[y][x]

    def __setitem__(self, coordinates, value):
        x, y = coordinates
        self.check_range(x, y)
        self._check_value(value)
        self._lines[y][x] = value

    def free(self, x, y):
        return self.is_type(x, y, '.')

    def elf(self, x, y):
        return self.is_type(x, y, 'E')

    def goblin(self, x, y):
        return self.is_type(x, y, 'G')

    def is_type(self, x, y, value):
        return self.in_range(x, y) and self[x, y] == value

    def in_range(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def _check(self):
        if len(self._lines) != self.height:
            raise ValueError()
        for line in self._lines:
            if len(line) != self.width:
                raise ValueError()

    def check_range(self, x, y):
        if not self.in_range(x, y):
            raise ValueError(
                'x: ' + str(x) + ', y: ' + str(y) +
                ', width: ' + str(self.width) + ', height: ' + str(self.height))

    def _check_value(self, value):
        if value not in '#.EG':
            raise ValueError('Illegal value [' + str(value) + ']')
