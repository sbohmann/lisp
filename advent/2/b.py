from io import open

def run():
    lines = []
    for raw_line in open('input.txt'):
        line = raw_line.strip()
        print('[' + line + ']')
        lines.append(line)
    solution = Solution(lines)
    print(solution.found_pair)
    if solution.found_pair:
        print(solution.first)
        print(solution.second)
        print(solution.result)


class Solution:
    def __init__(self, lines):
        self.lines = lines
        self.found_pair = False
        self._find_pair()
        self._create_result()

    def _find_pair(self):
        for first_index in range(0, len(self.lines) - 2):
            self._find_match(first_index)

    def _find_match(self, first_index):
        candidate = self.lines[first_index]
        for other_index in range(first_index, len(self.lines) - 1):
            other = self.lines[other_index]
            self._match_pair(candidate, other)

    def _match_pair(self, candidate, other):
        if self._pair_matches(candidate, other):
            if self.found_pair:
                raise ValueError('Found two matching pairs')
            self.found_pair = True
            self.first = candidate
            self.second = other

    def _pair_matches(self, a, b):
        single_mismatch = False
        for ca, cb in zip(a, b):
            if ca != cb:
                if single_mismatch:
                    single_mismatch = False
                    break
                else:
                    single_mismatch = True
        return single_mismatch

    def _create_result(self):
        if self.found_pair:
            self.result = self._collect_matching_characters(self.first, self.second)

    def _collect_matching_characters(self, a, b):
        return ''.join(map(lambda pair: pair[0] if pair[0] == pair[1] else '', zip(a, b)))


run()
