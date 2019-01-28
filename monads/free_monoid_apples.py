class Apple:
    def __init__(self, green, price):
        self.green = green
        self.price = price

    def __repr__(self):
        return 'Apple(green: ' + str(self.green) + ', price: ' + str(self.price) + ')'


def concat(a, b):
    result = []
    result.extend(a)
    result.extend(b)
    return result


a = [Apple(True, 3), Apple(False, 5)]
b = [Apple(True, 2)]

print(concat(a, b))
print(concat(a, b))
print(concat([], concat(a, b)))
print(concat(concat(a, b), []))
