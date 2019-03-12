from map_from_file import MapFromFile


class Solution:
    def __init__(self):
        self._map = MapFromFile('input.txt').result
        sum = 0
        for x in range(0, self._map.width):
            for y in range(0, self._map.height):
                if self._map.free(x, y):
                    sum += 1
        print(str(sum) + ' free positions')


Solution()