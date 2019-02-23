import math

import pygame

from agentData import Attributes
from vector import Vector
import client

class Renderer():
    _instance = None

    @staticmethod
    def Get():
        if Renderer._instance is None:
            Renderer._instance = Renderer()

        return Renderer._instance

    def __init__(self):
        pygame.display.init()
        self.size = Vector(800, 600)
        self.screen = pygame.display.set_mode(self.size.GetTuple(), pygame.DOUBLEBUF)
        self.camera = Vector(0.0, 0.0)

        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 20)

    def GetScreenPosition(self, position):
        delta = position - self.camera
        screenOffset = self.size // 2
        delta += screenOffset
        return delta 

    def Update(self, data):
        for agent in data['agents']:
            if client.Client.Get().userId == agent['user_id']:
                self.camera = Vector.FromTuple(agent['position'])
                break

        self.screen.fill((0, 0, 0))

        genericTriangle = [(10, 0), (-6, 6), (-6, -6)]
        missileTriangle = [(6, 0), (-3, 2), (-3, -2)]

        for agent in data['agents']:
            position = Vector.FromTuple(agent['position'])
            rotation = agent['rotation']
            race = agent[Attributes.RACE]
            agentClass = agent[Attributes.CLASS]
            level = agent[Attributes.LEVEL]
            triangle = []
            for vertex in genericTriangle:
                x = vertex[0] * math.cos(rotation) - vertex[1] * math.sin(rotation)
                y = vertex[0] * math.sin(rotation) + vertex[1] * math.cos(rotation)
                screenPosition = self.GetScreenPosition(Vector(x + position.x, y + position.y))
                triangle.append(screenPosition.GetTuple())

            pygame.draw.polygon(self.screen, (255, 255, 255), triangle)

            text = race + ' ' + agentClass + ' [' + str(level) + ']'  
            textSurface = self.font.render(text, False, (255, 255, 255))
            textSize = Vector.FromTuple(textSurface.get_size())
            textPosition = position - (textSize // 2)
            textPosition.y += 20.0
            textPosition = self.GetScreenPosition(textPosition)
            self.screen.blit(textSurface, textPosition.GetTuple())

        for missile in data['missiles']:
            rotation = missile['rotation']
            position = Vector(missile['x'], missile['y'])

            direction = Vector(math.cos(rotation), math.sin(rotation))

            for i in range(0, 20):
                triangle = []
                for vertex in missileTriangle:
                    x = vertex[0] * math.cos(rotation) - vertex[1] * math.sin(rotation)
                    y = vertex[0] * math.sin(rotation) + vertex[1] * math.cos(rotation)
                    triangle.append((x + 20.0, y + 20.0))

                surface = pygame.surface.Surface((40, 40), pygame.SRCALPHA)
                surface.fill((255, 0, 0, 0))

                factor = float(i - 10)

                alpha = math.exp(-math.pow(factor, 2.0) / 18.0) * 128.0
                pygame.draw.polygon(surface, (255, 255, 255, int(alpha)), triangle)

                deltaFactor = factor * 5.0
                surfacePosition = position + direction * deltaFactor - 20.0
                surfacePosition = self.GetScreenPosition(surfacePosition)
                self.screen.blit(surface, surfacePosition.GetTuple())

        pygame.display.flip()