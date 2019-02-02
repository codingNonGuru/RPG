import math

class Vector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def FromTuple(cls, dataTuple):
        return cls(dataTuple[0], dataTuple[1])

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __truediv__(self, factor):
        return Vector(self.x / factor, self.y / factor)

    def __floordiv__(self, factor):
        return Vector(self.x // factor, self.y // factor)

    def __sub__(self, other):
        if type(other) is Vector:
            return Vector(self.x - other.x, self.y - other.y)
        else:
            return Vector(self.x - other, self.y - other)

    def __mul__(self, factor):
        return Vector(self.x * factor, self.y * factor)

    def GetLength(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def GetTuple(self):
        return (self.x, self.y)

    @staticmethod
    def GetCrossProduct(first, second):
        return (first.x * second.y) - (first.y * second.x)