from io import open

def run():
    pairs = 0
    triples = 0
    for raw_line in open('input.txt'):
        line = raw_line.strip()
        print('[' + line + ']')
        count = LetterCount(line)
        print('pair: ', count.has_pair, ', triple: ', count.has_triple, sep = '')
        if count.has_pair:
            pairs += 1
        if count.has_triple:
            triples += 1
    print('pairs: ', pairs, ', triples: ', triples, ', checksum: ', pairs * triples, sep = '')


class LetterCount:
    def __init__(self, text):
        self.text = text
        self.build_frequency_map()
        self.create_result()

    def build_frequency_map(self):
        self._frequency_map = {}
        for c in self.text:
            if c not in self._frequency_map:
                self._frequency_map[c] = 1
            else:
                count = self._frequency_map[c]
                self._frequency_map[c] = count + 1

    def create_result(self):
        self.has_pair = False
        self.has_triple = False
        for value in self._frequency_map.values():
            if value == 2:
                self.has_pair = True
            elif value == 3:
                self.has_triple = True


run()
