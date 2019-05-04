import random

import agent
from agentData import Attributes, Races
from vector import Vector

import math

class AgentFactory():
    _instance = None

    @staticmethod
    def Get():
        if AgentFactory._instance is None:
            AgentFactory._instance = AgentFactory()

        return AgentFactory._instance

    def GetAgent(self, controllerData, characterData, faction, spawnData = None):
        characterData[Attributes.LEVEL] = random.randint(1, 10)

        dice = random.randint(0, 100)
        if dice < 30:
            characterData[Attributes.RACE] = Races.DWARF
        elif dice < 60:
            characterData[Attributes.RACE] = Races.ORC
        else:
            characterData[Attributes.RACE] = Races.HUMAN

        position = None

        if spawnData is None:
            position = Vector(random.random() * 600.0 - 300.0, random.random() * 600.0 - 300.0)
        else:
            angle = random.random() * 6.2831
            radius = random.random() * spawnData.areaSize
            positionOffset = Vector(math.cos(angle) * radius, math.sin(angle) * radius)
            position = spawnData.position + positionOffset

        newAgent = agent.Agent(position, controllerData, characterData, faction)

        #if characterData['race'] is Races.DWARF:
        #   characterData['strength'] = 4
        #   characterData['reflexes'] = 1
        #   characterData['perception'] = 2
        #   characterData['willpower'] = 4
        #   characterData['intelligence'] = 2
        #   characterData['charisma'] = 2
        #else:
        
        return newAgent