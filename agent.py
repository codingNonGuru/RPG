import math
import random

import scene
from engine import Engine
from missile import Missile

class Agent:
    def __init__(self, controller):
        self.controller = controller
        self.x = random.random() * 800.0
        self.y = random.random() * 600.0
        self.rotation = random.random() * 6.2831
        self.cooldown = 0.0
        self.hitpointCount = 5

    def Fire(self):
        if self.cooldown < 2.0:
            return

        self.cooldown = 0.0
        missile = Missile(self)
        scene.Scene.Get().missiles.append(missile)

    def Move(self, direction):
        if self.hitpointCount <= 0:
            return 
            
        if direction == 'rightwards':
            self.rotation -= 0.02
        elif direction == 'leftwards':
            self.rotation += 0.02

        if 'forward' == direction:
            self.x += math.cos(self.rotation)
            self.y += math.sin(self.rotation)
        elif 'backwards' == direction:
            self.x -= math.cos(self.rotation)
            self.y -= math.sin(self.rotation)

    def Update(self):
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

        x = self.x - other.x
        y = self.y - other.y
        distance = math.sqrt(x * x + y * y)

        return distance < 10.0

    def Damage(self):
        if self.hitpointCount <= 0:
            return 

        self.hitpointCount -= 1