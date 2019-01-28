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

        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 20)

    def Update(self, data):
        self.screen.fill((0, 0, 0))

        genericTriangle = [(10, 0), (-6, 6), (-6, -6)]
        missileTriangle = [(6, 0), (-3, 2), (-3, -2)]

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

            textSurface = self.font.render('Aloha', False, (255, 255, 255))
            textSize = textSurface.get_size()
            textPosition = (position[0] - textSize[0] / 2, position[1] - textSize[1] / 2 + 20)
            self.screen.blit(textSurface, textPosition)

        for missile in data['missiles']:
            rotation = missile['rotation']
            position = (missile['x'], missile['y'])

            direction = (math.cos(rotation), math.sin(rotation))

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
                surfacePosition = (int(position[0] + direction[0] * deltaFactor - 20.0), int(position[1] + direction[1] * deltaFactor - 20.0))
                self.screen.blit(surface, surfacePosition)

        pygame.display.flip()