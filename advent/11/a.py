from multiprocessing import Pool
import numpy
import threading


input = 3999
parallel = True

def run():
    maximum = None
    position = None
    size = None
    cells = calculate_cells()
    progress = AtomicInteger()
    report_progress = lambda: print_progress(progress)
    if parallel:
        maximum, position, size = solve_in_parallel(cells, maximum, position, size, report_progress)
    else:
        maximum, position, size = solve_sequentially(cells, maximum, position, size, report_progress)
    print(maximum, size, position)


def print_progress(progress):
    progress.increment()
    print(str(int(100.0 * progress.value / 300.0 + 0.5)) + '%')


class AtomicInteger:
    def __init__(self):
        self._lock = threading.Lock()
        self.value = 0

    def increment(self):
        self._lock.acquire()
        try:
            self.value += 1
        finally:
            self._lock.release()


def solve_sequentially(cells, maximum, position, size, report_progress):
    for square_size in range(1, 301):
        result_for_size = MaximumSquare(square_size, cells)
        report_progress()
        if maximum is None or result_for_size.maximum > maximum:
            maximum = result_for_size.maximum
            position = result_for_size.position
            size = square_size
    return maximum, position, size


def solve_in_parallel(cells, maximum, position, size, report_progress):
    results = Pool(8).imap_unordered(calculate_for_size,
                          map(lambda square_size: (square_size, cells), range(1, 301)))
    for result in results:
        report_progress()
        if maximum is None or result.maximum > maximum:
            maximum = result.maximum
            position = result.position
            size = result.square_size
    return maximum, position, size


def calculate_for_size(input):
    square_size, cells = input
    result = MaximumSquare(square_size, cells)
    return result


def calculate_cells():
    result = [0] * (300 * 300)
    for y in range(1, 301):
        for x in range(1, 301):
            result[(y - 1) * 300 + (x - 1)] = calculate_cell(x, y)
    return numpy.array(result)


def calculate_cell(x, y):
    rack_id = x + 10
    raw_result = (rack_id * y + input) * rack_id
    result = (raw_result // 100) % 10 - 5
    return result


class MaximumSquare:
    def __init__(self, square_size, cells):
        self.square_size = square_size
        self._cells = cells
        self._find_maximum_square()

    def _find_maximum_square(self):
        maximum = None
        top_left = None
        for y in range(1, 302 - self.square_size):
            for x in range(1, 302 - self.square_size):
                value = self._calculate_square(x, y)
                if maximum is None or value > maximum:
                    maximum = value
                    top_left = (x, y)
        self.maximum = maximum
        self.position = top_left


    def _calculate_square(self, x, y):
        if x > 1:
            result = self._adjust_last_sum(x, y)
        else:
            result = self._calculate_square_from_scratch(x, y)
        self._last_sum = result
        return result

    def _adjust_last_sum(self, x, y):
        start_offset = self._offset(x, y)
        end_offset = self._offset(x, y + self.square_size)
        left_column = numpy.sum(self._cells[start_offset:end_offset:300])

        result = self._last_sum - left_column

        last_x = x + self.square_size - 1
        start_offset = self._offset(last_x, y)
        end_offset = self._offset(last_x, y + self.square_size)
        result += numpy.sum(self._cells[start_offset:end_offset:300])
        return result

    def _calculate_square_from_scratch(self, x, y):
        sum = 0
        for dy in range(0, self.square_size):
            start_offset = self._offset(x, y + dy)
            end_offset = start_offset + self.square_size
            sum += numpy.sum(self._cells[start_offset:end_offset])
        return sum

    def _cell(self, x, y):
        return self._cells[self._offset(x, y)]

    def _offset(self, x, y):
        return (y - 1) * 300 + (x - 1)


run()
