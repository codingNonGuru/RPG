import math
import random

import scene
from engine import Engine
from missile import Missile
import controller
from vector import Vector
from body import Body

class Agent(Body):
    def __init__(self, controllerData, faction):
        position = Vector(random.random() * 800.0, random.random() * 600.0)
        rotation = random.random() * 6.2831
        super(Agent, self).__init__(position, rotation)

        if controllerData['isHuman']:
            self.controller = controller.HumanController(self, controllerData['id'])
        else:
            self.controller = controller.MachineController(self)
        
        self.cooldown = 0.0
        self.hitpointCount = 5

        self.faction = faction
        self.speedModifier = 2.0

    def Fire(self):
        if self.cooldown < 5.0:
            return

        self.cooldown = 0.0
        missile = Missile(self)
        scene.Scene.Get().missiles.append(missile)

    def Move(self, direction):
        if self.hitpointCount <= 0:
            return 
            
        if direction == 'rightwards':
            self.rotation -= 0.05
        elif direction == 'leftwards':
            self.rotation += 0.05

        if 'forward' == direction:
            self.position += self.GetForward() * self.speedModifier
        elif 'backwards' == direction:
            self.position -= self.GetForward() * self.speedModifier

    def Update(self):
        if self.hitpointCount <= 0:
            return

        self.controller.Update()

        if self.controller.isMoving:
            self.Move(self.controller.moveDirection)

        if self.controller.isTurning:
            self.Move(self.controller.turnDirection)

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