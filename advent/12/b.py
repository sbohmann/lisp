from io import open
import re
from offset_list import OffsetList


setup_pattern = re.compile('initial state: ([#.]*)')
rule_pattern = re.compile('([#.]{5}) => ([#.])')


def run():
    file = open('input.txt')
    setup = read_setup(file)
    rules = read_rules(file)
    solution = Solution(setup, rules)
    print(solution.result)


def read_setup(file):
    line = file.readline().strip()
    match = setup_pattern.fullmatch(line)
    if match is None or file.readline().strip() != '':
        raise ValueError()
    setup = interpret(match[1])
    result = OffsetList(False, 0, size=len(setup))
    for index in range(0, len(setup)):
        result[index] = setup[index]
    for index in result.range():
        print(index, result[index])
    return result


def read_rules(file):
    result = {}
    for line in file:
        line = line.strip()
        if line != '':
            key, value = read_rule(line)
            result[key] = value
    return result


def read_rule(line):
    match = rule_pattern.fullmatch(line)
    return interpret(match[1]), interpret_char(match[2])


def interpret(textual_representation):
    result = []
    for c in textual_representation:
        result.append(interpret_char(c))
    return tuple(result)


def interpret_char(c):
    if c == '#':
        return True
    elif c == '.':
        return False
    else:
        raise ValueError()


class Solution:
    def __init__(self, setup, rules):
        self._setup = setup
        self._rules = rules
        self._found_result = False
        self._hash = None
        self._calculate()

    def _calculate(self):
        self._state = self._setup
        print(''.join(map(str, self._state.to_list())))
        for n in range(1, 10_0001):
            self._calculate_new_state()
            if self._found_result:
                print('found result in round', n)
                break
            if n % 1000 == 0:
                self.result, _ = self._determine_result()
                reduced_result, _ = self._determine_result(n)
                adjusted_result, num_true = self._determine_result(n, 50_000_000_000)
                print(n, ':', self.result, adjusted_result, self.result, num_true, len(self._state), self._state.start(), self._state.stop(),
                      ''.join(map(str, self._state.to_list())))
        print(len(self._state), self._state.start(), self._state.stop(),''.join(map(str, self._state.to_list())))
        self.result = self._determine_result()

    def _calculate_new_state(self):
        offset = self._state.start() - 2
        size = len(self._state) + 4
        new_state = OffsetList(False, offset, size)
        first = None
        last = None
        new_hash = 0
        for index in new_state.range():
            value = self._determine_value(index)
            if value:
                if first is None:
                    first = index
                last = index
                new_state[index] = True
                new_hash += index
        if new_hash == self._hash:
            equal = True
            for index in new_state.range():
                if new_state[index] == self._state[index]:
                    equal = False
                    break
            if equal:
                print('equal!')
                self._found_result = True
        if last - first < size // 2:
            # print('first:', first, 'last:', last)
            new_state = new_state.partition(first, last - first + 1)
            # print(len(new_state), new_state.start(), new_state.stop(), ''.join(map(str, new_state.to_list())))
        self._state = new_state
        self._hash = new_hash

    def _determine_value(self, index):
        key = tuple(self._state.part(index - 2, index + 3))
        value = self._rules[key]
        return value

    def _determine_result(self, n=0, m=0):
        result = 0
        num_true = 0
        for index in range(self._state.start(), self._state.stop()):
            if self._state[index]:
                # print(index, index - n, index - n + m)
                result += index - n + m
                num_true += 1
        return result, num_true

run()
