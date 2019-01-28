class OffsetList:
    def __init__(self, default_value, offset, size=0, **kwargs):
        self._default_value = default_value
        self._offset = offset
        self._data = kwargs.get('_data', [default_value] * size)

    def start(self):
        return self._offset

    def stop(self):
        return self._offset + len(self._data)

    def __getitem__(self, index):
        if self._offset <= index < self._offset + len(self._data):
            return self._data[index - self._offset]
        else:
            return self._default_value

    def __setitem__(self, index, value):
        self._data[index - self._offset] = value

    def __len__(self):
        return len(self._data)

    def range(self):
        return range(self._offset, self._offset + len(self._data))

    def to_list(self):
        return self._data.copy()

    def part(self, start, stop):
        result = [self._default_value] * (stop - start)
        for index in range(start, stop):
            result[index - start] = self[index]
        return result

    def partition(self, offset, size):
        relative_offset = offset - self._offset
        return OffsetList(False, offset, size, _data=list(self._data[relative_offset:relative_offset + size]))
