import time

import pygame

import client as clientModule
import renderer as rendererModule

class Engine():
    _instance = None

    @staticmethod
    def Get():
        if Engine._instance is None:
            Engine._instance = Engine()

        return Engine._instance

    def __init__(self):
        rendererModule.Renderer.Get()

        self.moveFactor = 0.0
        self.turnFactor = 0.0

        self.frameDelta = 0.0

    def Start(self):
        lastClock = time.clock()
        while True:
            self.frameDelta = time.clock() - lastClock
            self.frameDelta *= 100.0
            lastClock = time.clock()

            self.Update()

    def Update(self):
        pygame.event.pump()
        pressedKeys = pygame.key.get_pressed()

        if pressedKeys[pygame.K_ESCAPE]:
            pygame.quit()
            return

        client = clientModule.Client.Get()

        self.moveFactor = 0.0
        if pressedKeys[pygame.K_w]:
            self.moveFactor += self.frameDelta
        elif pressedKeys[pygame.K_s]:
            self.moveFactor -= self.frameDelta

        self.turnFactor = 0.0
        if pressedKeys[pygame.K_a]:
            self.turnFactor -= self.frameDelta
        elif pressedKeys[pygame.K_d]:
            self.turnFactor += self.frameDelta

        if pressedKeys[pygame.K_SPACE]:
            client.SendPlayerFiredMessage()

        client.SendPlayerMovedMessage(self.moveFactor)
        client.SendPlayerTurnedMessage(self.turnFactor)

        message = client.GetMessage()

        rendererModule.Renderer.Get().Update(message)