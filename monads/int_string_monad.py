# a is string, m is int

def unit(a):
    return int(a)

def bind(f, g):
    return lambda x: g(str(f(x)))

def f(a):
    return unit(a) * 3

def g(a):
    return unit(a) + 7

print(f('5'))
print(bind(unit, f)('5'))
print(bind(f, unit)('5'))

print(g('5'))
print(bind(unit, g)('5'))
print(bind(g, unit)('5'))

print(bind(f, g)(5))
print(bind(g, f)(5))
