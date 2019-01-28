from io import open
import re
from flexlist import FlexList


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
    result = FlexList(False)
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
        self._calculate()

    def _calculate(self):
        self._state = self._setup
        print(''.join(map(str, self._state.to_list())))
        for n in range(0, 20):
            self._calculate_new_state()
        print(len(self._state), self._state.start(), self._state.stop(),''.join(map(str, self._state.to_list())))
        self.result = self._determine_result()

    def _calculate_new_state(self):
        new_state = FlexList(False, start=self._state.start(), stop=self._state.stop())
        for index in range(self._state.start() - 2, self._state.stop() + 2):
            value = self._determine_value(index)
            if value:
                new_state[index] = True
        self._state = new_state

    def _determine_value(self, index):
        key = tuple(self._state.part(index - 2, index + 3))
        value = self._rules[key]
        return value

    def _determine_result(self, n=0, m=0):
        result = 0
        for index in range(self._state.start(), self._state.stop()):
            if self._state[index]:
                result += index - n + m
        return result


run()
