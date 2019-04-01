class BoundedList:
    def __init__(self, size):
        self.size = size
        self.values = [0 for _ in range(0, self.size)]

    def add_value(self, value):
        self.values[0:self.size - 1] = self.values[1:]
        self.values[-1] = value

    def max(self):
        return max(self.values)

    def min(self):
        return min(self.values)

    def __str__(self):
        return self.values.__str__()

    def __repr__(self):
        return self.values.__repr__()

    def __gt__(self, other):
        return self.values.__gt__(other.values)

    def __getitem__(self, item):
        return self.values.__getitem__(item)
