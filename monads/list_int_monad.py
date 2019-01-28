from functools import reduce

# a: [], m: int

def unit(a):
    return len(a)

def bind(f, g):
    return lambda x: bind_to_value(f(x), g)

def bind_to_value(m, g):
    return m + g([m])

def f(a):
    return reduce(lambda sum, value: sum + value, a, 0)

print(f([1, 2, 3]))
print(bind(unit, f)([1, 2, 3]))
print(bind(f, unit)([1, 2, 3]))
