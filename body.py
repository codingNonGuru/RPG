import math

from vector import Vector

class Body(object):
    def __init__(self, position, rotation):
        self.position = position
        self.rotation = rotation

    def GetForward(self):
        return Vector(math.cos(self.rotation), math.sin(self.rotation))