def unit(a):
    return [a]

def bind(f, g):
    return lambda x: bind_to_instance(f(x), g)

def bind_to_instance(m, g):
    result = []
    for value in m:
        result.extend(g(value))
    return result


# examples

def f(a):
    return [a, a, a]

def g(a):
    return list(range(0, a))

print(f(3))
print(bind(unit, f)(3))
print(bind(f, unit)(3))

print(g(3))
print(bind(unit, g)(3))
print(bind(g, unit)(3))

print(bind(f, g)(3))
print(bind(g, f)(3))

def h(a):
    return [a + 7, a + 9]

print(bind(bind(f, g), h)(3))
print(bind(f, bind(g, h))(3))
print(bind(bind(g, f), h)(3))
print(bind(g, bind(f, h))(3))
print(bind(bind(f, h), g)(3))
print(bind(f, bind(h, g))(3))
