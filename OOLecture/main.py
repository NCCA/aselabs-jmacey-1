class Number:
    def __init__(self, value):
        self.value = value

    def square(self):
        self.value = self.value * self.value


a = Number(10)
b = Number(2)

a.square()
print(a.value)
print(b.value)
