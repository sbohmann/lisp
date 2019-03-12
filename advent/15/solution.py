from map_from_file import MapFromFile
from flood_search import FloodSearch


class Solution:
    def __init__(self):
        self._map = MapFromFile('input.txt').result


Solution()
