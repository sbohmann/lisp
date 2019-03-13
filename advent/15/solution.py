from map_from_file import MapFromFile
from flood_search import FloodSearch


class Solution:
    def __init__(self):
        self._map = MapFromFile('input.txt').result
        while not self._stop():
            pass

    def _stop(self):
        elves = self._map.count(lambda x, y, field_type: field_type == 'E')
        goblins = self._map.count(lambda x, y, field_type: field_type == 'G')
        return elves == 0 or goblins == 0


Solution()
