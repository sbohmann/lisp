from map_from_file import MapFromFile
from flood_search import FloodSearch

situation = MapFromFile('test-input.txt').result
search = FloodSearch(situation, (2, 2))
