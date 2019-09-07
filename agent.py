import math
import random

import scene
from engine import Engine
from missile import Missile
import controller
from vector import Vector
from body import Body
from agentData import Attributes

DEVIATION_MODIFIER = 0.15

class Agent(Body):
    def __init__(self, position, controllerData, characterData, faction):
        rotation = random.random() * 6.2831
        super(Agent, self).__init__(position, rotation)

        if controllerData['isHuman']:
            self.controller = controller.HumanController(self, controllerData['id'])
        else:
            self.controller = controller.MachineController(self)
        
        self.reflexes = 2

        self.cooldown = 0.0
        self.hitpointCount = 5

        self.faction = faction
        self.moveSpeedModifier = 5.0
        self.turnSpeedModifier = 0.02

        self.characterData = characterData

    def Fire(self):
        if self.cooldown < 5.0:
            return

        self.cooldown = 0.0

        deviationFactor = float(10 - self.reflexes) * 0.1
        if deviationFactor < 0.0:
            deviationFactor = 0.0
        deviationFactor *= DEVIATION_MODIFIER

        deviation = random.random() * (2.0 * deviationFactor) - deviationFactor
        rotation = self.rotation + deviation
        missile = Missile(self, rotation)
        scene.Scene.Get().missiles.append(missile)

    def Move(self, factor):
        if self.hitpointCount <= 0:
            return 

        self.position += self.GetForward() * self.moveSpeedModifier * factor

    def Turn(self, factor):
        if self.hitpointCount <= 0:
            return 
            
        self.rotation += factor * self.turnSpeedModifier

        if self.rotation > 6.2831:
            self.rotation -= 6.2831
        elif self.rotation < 0.0:
            self.rotation += 6.2831

    def Update(self):
        if self.hitpointCount <= 0:
            return

        self.controller.Update()

        if self.controller.isMoving:
            self.Move(self.controller.moveDirection)

        if self.controller.isTurning:
            self.Turn(self.controller.turnDirection)

        if self.controller.isShooting:
            self.Fire()

        self.cooldown += Engine.Get().frameDelta

    def CheckCollision(self, other):
        if self is other.owner:
            return False

        if self.hitpointCount <= 0:
            return False 

        if other.IsDestroyable():
            return False

        direction = other.position - self.position
        distance = direction.GetLength()

        return distance < 10.0

    def Damage(self):
        if self.hitpointCount <= 0:
            return 

        self.hitpointCount -= 1