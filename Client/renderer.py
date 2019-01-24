import math

import pygame

class Renderer():
    _instance = None

    @staticmethod
    def Get():
        if Renderer._instance is None:
            Renderer._instance = Renderer()

        return Renderer._instance

    def __init__(self):
        pygame.display.init()
        self.size = (800, 600)
        self.screen = pygame.display.set_mode(self.size, pygame.DOUBLEBUF)

    def Update(self, data):
        self.screen.fill((0, 0, 0))

        genericTriangle = [(10, 0), (-6, 6), (-6, -6)]

        index = 0
        for position in data['positions']:
            rotation = data['rotations'][index]
            triangle = []
            for vertex in genericTriangle:
                x = vertex[0] * math.cos(rotation) - vertex[1] * math.sin(rotation)
                y = vertex[0] * math.sin(rotation) + vertex[1] * math.cos(rotation)
                triangle.append((x + position[0], y + position[1]))

            pygame.draw.polygon(self.screen, (255, 255, 255), triangle)
            index += 1

        for missile in data['missiles']:
            rotation = missile['rotation']
            position = (missile['x'], missile['y'])
            triangle = []
            for vertex in genericTriangle:
                x = vertex[0] * math.cos(rotation) - vertex[1] * math.sin(rotation)
                y = vertex[0] * math.sin(rotation) + vertex[1] * math.cos(rotation)
                x *= 0.5
                y *= 0.5
                triangle.append((x + position[0], y + position[1]))

            pygame.draw.polygon(self.screen, (255, 255, 255), triangle)

        pygame.display.flip()