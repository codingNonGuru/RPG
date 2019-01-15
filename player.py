import random

from scene import Scene
from engine import Engine
from missile import Missile

class Player:
    def __init__(self, id):
        self.id = id
        self.x = random.random() * 800.0
        self.y = random.random() * 600.0
        self.rotation = random.random() * 6.2831
        self.cooldown = 0.0

    def Fire(self):
        if self.cooldown < 2.0:
            return

        self.cooldown = 0.0
        missile = Missile(self)
        Scene.Get().missiles.append(missile)

    def Update(self):
        self.cooldown += Engine.Get().frameDelta