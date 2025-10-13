import sys


class RunningTotal:
    def __init__(self):
        self.min = sys.maxsize
        self.max = -sys.maxsize - 1
        self.total = 0
        self.count = 0

    @classmethod
    def from_list(cls, values):
        t = cls()
        for v in values:
            t.add_number(v)
        return t

    def __str__(self):
        return f"{self.min=} {self.max=} {self.total=} {self.count=}"

    def _check_min_max(self, value):
        if value >= self.max:
            self.max = value
        if value <= self.min:
            self.min = value

    def add_number(self, value):
        self.total += value
        self.count += 1
        self._check_min_max(value)

    def average(self):
        try:
            return self.total / self.count
        except ZeroDivisionError:
            print("trying to divide by zero")
            raise
