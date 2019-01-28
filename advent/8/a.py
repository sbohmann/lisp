from io import open
from functools import reduce


def run():
    line = open('input.txt').readline().strip()
    numbers = line.split()
    iterator = iter(numbers)
    root = NodeParser(iterator).result
    check_end(iterator)
    sum = 0
    for value in root.all_metadata():
        sum += value
    print('sum:', sum)
    print(NodeValue(root).result)


def check_end(iterator):
    if next(iterator, None) is not None:
        raise ValueError()


class NodeParser:
    def __init__(self, iterator):
        self._iterator = iterator
        self._read_header()
        self._read_subnodes()
        self._read_metadata()
        self.result = Node(self._subnodes, self._metadata)

    def _read_header(self):
        self._number_of_subnodes = self._next()
        self._metadata_size = self._next()

    def _read_subnodes(self):
        self._subnodes = [None] * self._number_of_subnodes
        for index in range(0, self._number_of_subnodes):
            self._subnodes[index] = NodeParser(self._iterator).result

    def _read_metadata(self):
        self._metadata = [None] * self._metadata_size
        for index in range(0, self._metadata_size):
            self._metadata[index] = self._next()

    def _next(self):
        return int(next(self._iterator))


class Node:
    def __init__(self, subnodes, metadata):
        self.subnodes = subnodes
        self.metadata = metadata

    def all_metadata(self):
        for value in self.metadata:
            yield value
        for subnode in self.subnodes:
            for value in subnode.all_metadata():
                yield value


class NodeValue:
    def __init__(self, node):
        self.node = node
        if len(node.subnodes) == 0:
            self.create_simple_result()
        else:
            self._create_indexed_result()

    def create_simple_result(self):
        self.result = reduce(lambda sum, value: sum + value, self.node.metadata, 0)

    def _create_indexed_result(self):
        self.result = 0
        for index in self.node.metadata:
            self.result += self._value_for_index(index)

    def _value_for_index(self, index):
        if index > 0 and index <= len(self.node.subnodes):
            return NodeValue(self.node.subnodes[index - 1]).result
        else:
            return 0


run()
