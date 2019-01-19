import math

class Missile:
    def __init__(self, shooter):
        self.x = shooter.x
        self.y = shooter.y
        self.rotation = shooter.rotation
        self.lifetime = 0.0
        self.speedModifier = 100.0
        self.hitpointCount = 1
        self.owner = shooter

    def Update(self, deltaTime):
        self.lifetime += deltaTime

        self.x += math.cos(self.rotation) * deltaTime * self.speedModifier
        self.y += math.sin(self.rotation) * deltaTime * self.speedModifier

    def IsDestroyable(self):
        return self.lifetime > 5.0 or self.hitpointCount <= 0

    def Damage(self):
        self.hitpointCount -= 1