def unit(x):
    return x


def bind(f, g):
    return lambda x: g(f(x))


# examples
def f(x):
    return x + 3

def g(x):
    return x * 5

print(f(7))
print(bind(unit, f)(7))
print(bind(f, unit)(7))

print(g(7))
print(bind(unit, g)(7))
print(bind(g, unit)(7))

print('f, g', bind(f, g)(7))
print('g, f', bind(g, f)(7))

print(bind(f, bind(g, f))(7))
print(bind(bind(f, g), f)(7))
