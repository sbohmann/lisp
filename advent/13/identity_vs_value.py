from vehicle import Vehicle

a = Vehicle(1, 2, 3)
b = Vehicle(1, 2, 3)

s = set()
s.add(a)
s.add(b)

print(s)
b.direction = 1
s.remove(b)
print(s)

l = [a, b]
print(l)
a.direction = 2
l.remove(a)
print(l)
