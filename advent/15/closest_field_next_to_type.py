from functools import cmp_to_key

import reading_order
from flood_search import FloodSearch, offsets, add


class ClosestFieldNextToType:
    def __init__(self, situation, position, field_type):
        self._situation = situation
        self._field_type = field_type
        self._candidates = []
        self.result = None
        self._search = FloodSearch(situation, position)
        self._calculate()

    def _calculate(self):
        self._collect_positions()
        self._select_candidate()

    def _collect_positions(self):
        for y in range(0, self._situation.height):
            for x in range(0, self._situation.width):
                self._evaluate_position(x, y)

    def _evaluate_position(self, x, y):
        distance = self._search[x, y]
        if self._is_candidate(x, y, distance):
            self._candidates.append(Candidate(x, y, distance))

    def _is_candidate(self, x, y, distance):
        return distance is not None and self._neighboring_type_matches(x, y)

    def _neighboring_type_matches(self, x, y):
        for offset in offsets:
            other_x, other_y = add((x, y), offset)
            return self._situation.is_type(other_x, other_y, self._field_type)

    def _select_candidate(self):
        if self._candidates:
            minimum_distance = min(self._candidates, key=lambda candidate: candidate.distance)
            filtered = filter(lambda candidate: candidate.distance == minimum_distance)
            filtered.sort(key=cmp_to_key(compare_candidates_by_position))
            self._result = filtered[0]


class Candidate:
    def __init__(self, x, y, distance):
        self.position = x, y
        self.distance = distance


def compare_candidates_by_position(a, b):
    return reading_order.compare(a.position, b.position)
