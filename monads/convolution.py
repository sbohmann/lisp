import math

# a function takes an Int and yields up Maximum samples of type Double
Maximum = 1_000_000
SamplesPerSecond = 100_000


def bind(f, g):
    return lambda index: _convolved(f, g, index)


def _convolved(f, g, index):
    sum = 0
    for offset in range(0, index):
        sum += f(offset) * g(index - offset)


def zero(index):
    return 1.0 if index == 0 else 0.0


def sin(index, frequency):
    if 0 <= index < Maximum:
        return math.sin(frequency * index / SamplesPerSecond)


def sin(frequency):
    return lambda index: sin(index, frequency)
