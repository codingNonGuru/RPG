import math

from body import Body

class Missile(Body):
    def __init__(self, shooter, rotation):
        super(Missile, self).__init__(shooter.position, rotation)
        self.lifetime = 0.0
        self.speedModifier = 70.0
        self.hitpointCount = 1
        self.owner = shooter

    def Update(self, deltaTime):
        self.lifetime += deltaTime

        self.position += self.GetForward() * deltaTime * self.speedModifier

    def IsDestroyable(self):
        return self.lifetime > 10.0 or self.hitpointCount <= 0

    def Damage(self):
        self.hitpointCount -= 1