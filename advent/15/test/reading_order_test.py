from unittest import TestCase, main
from functools import cmp_to_key

import reading_order


class ReadingOrderTest(TestCase):
    def test_sorting(self):
        positions = [(0, 0), (-9, -12), (3, 5), (5, 3), (1, 2), (2, 1), (1, 0), (0, 1)]
        positions.sort(key=cmp_to_key(reading_order.compare))
        self.assertEqual(
            positions,
            [(-9, -12), (0, 0), (1, 0), (0, 1), (2, 1), (1, 2), (5, 3), (3, 5)])


main()
