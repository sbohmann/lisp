class Apple:
    def __init__(self, green, price, next_apple=None):
        self.green = green
        self.price = price
        self.next_apple = next_apple

    def with_next_apple(self, next):
        if self.next_apple is None:
            return Apple(self.green, self.price, next_apple=next)
        else:
            return self.with_next_apple(next.next_apple)

a = Apple(True, 3).with_next_apple(Apple(False, 5).with_next_apple(Apple(True, 2)))

def combine(a, b):
    if a is None:
        return b
    else:
        return a.with_next_apple(b)
