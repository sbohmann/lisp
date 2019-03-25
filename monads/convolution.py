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


def wave(frequency, trigonometric_function):
    return lambda index: _wave(frequency, trigonometric_function, index)


def _wave(frequency, trigonometric_function, index):
    if 0 <= index < Maximum:
        return trigonometric_function(frequency * index / SamplesPerSecond)


def sin(frequency):
    return wave(frequency, math.sin)


def cos(frequency):
    return wave(frequency, math.cos)


def plus(f, g):
    return lambda index: f(index) + g(index)
