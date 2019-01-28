class FlexList:
    def __init__(self, default_value, **kwargs):
        self._default_value = default_value
        self._positive_data = kwargs.get('_positive_data', None)
        self._negative_data = kwargs.get('_negative_data', None)
        if self._positive_data is None:
            stop = kwargs.get("stop", 0)
            if stop > 0:
                self._positive_data = [default_value] * stop
            else:
                self._positive_data = []
        if self._negative_data is None:
            start = kwargs.get("start", 0)
            if start < 0:
                self._negative_data = [default_value] * (-start)
            else:
                self._negative_data = []

    def __len__(self):
        return len(self._positive_data) + len(self._negative_data)

    def start(self):
        return -len(self._negative_data)

    def stop(self):
        return len(self._positive_data)

    def range(self):
        return range(self.start(), self.stop())

    def copy(self):
        return FlexList(
            self._default_value,
            _positive_data=self._positive_data.copy(),
            _negative_data=self._negative_data.copy())

    def __getitem__(self, index):
        if index < 0:
            offset = - index
            if offset > len(self._negative_data):
                return self._default_value
            else:
                return self._negative_data[offset - 1]
        else:
            if index >= len(self._positive_data):
                return self._default_value
            else:
                return self._positive_data[index]

    def part(self, start, stop):
        result = [self._default_value] * (stop - start)
        for index in range(start, stop):
            result[index - start] = self[index]
        return result

    def to_list(self):
        return self.part(self.start(), self.stop())

    def __setitem__(self, index, value):
        if index < 0:
            offset = - index
            if offset > len(self._negative_data):
                offset -= 1
                self._expand(self._negative_data, offset, value)
            else:
                self._negative_data[offset - 1] = value
        else:
            if index >= len(self._positive_data):
                self._expand(self._positive_data, index, value)
            else:
                self._positive_data[index] = value

    def _expand(self, data, index, value):
        data += [self._default_value] * (index - len(data))
        data.append(value)
