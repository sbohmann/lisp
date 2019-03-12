class FindSequence:
    def __init__(self, data, sequence, last_len) -> None:
        self._data = data
        self._sequence = sequence
        self._last_len = last_len
        self.result = None
        self._search()

    def _search(self):
        for index in range(self._start(), len(self._data) - len(self._sequence) + 1):
            if self._match(index):
                break

    def _match(self, index):
        for offset in range(0, len(self._sequence)):
            if self._data[index + offset] != self._sequence[offset]:
                return False
        self.result = index
        return True

    def _start(self):
        return max(0, self._last_len - len(self._sequence))
