import math

class Missile:
    def __init__(self, shooter):
        self.x = shooter.x
        self.y = shooter.y
        self.rotation = shooter.rotation
        self.lifetime = 0.0
        self.speedModifier = 50.0

    def Update(self, deltaTime):
        self.lifetime += deltaTime

        self.x += math.cos(self.rotation) * deltaTime * self.speedModifier
        self.y += math.sin(self.rotation) * deltaTime * self.speedModifier

    def IsDestroyable(self):
        return self.lifetime > 5.0