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

    def Start(self):
        while True:
            self.Update()
    
    def Update(self):
        pygame.event.pump()
        pressedKeys = pygame.key.get_pressed()

        if pressedKeys[pygame.K_ESCAPE]:
            pygame.quit()
            return

        client = clientModule.Client.Get()

        if pressedKeys[pygame.K_w]:
            client.SendPlayerMovedMessage('forward')    
        elif pressedKeys[pygame.K_s]:
            client.SendPlayerMovedMessage('backwards')

        if pressedKeys[pygame.K_a]:
            client.SendPlayerMovedMessage('rightwards')
        elif pressedKeys[pygame.K_d]:
            client.SendPlayerMovedMessage('leftwards')

        if pressedKeys[pygame.K_SPACE]:
            client.SendPlayerFiredMessage()

        message = client.GetMessage()

        rendererModule.Renderer.Get().Update(message)