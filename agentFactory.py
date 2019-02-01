import random

import agent
from agentData import Attributes, Races

class AgentFactory():
    _instance = None

    @staticmethod
    def Get():
        if AgentFactory._instance is None:
            AgentFactory._instance = AgentFactory()

        return AgentFactory._instance

    def GetAgent(self, controllerData, characterData, faction):
        characterData[Attributes.LEVEL] = random.randint(1, 10)

        dice = random.randint(0, 100)
        if dice < 30:
            characterData[Attributes.RACE] = Races.DWARF
        elif dice < 60:
            characterData[Attributes.RACE] = Races.ORC
        else:
            characterData[Attributes.RACE] = Races.HUMAN

        newAgent = agent.Agent(controllerData, characterData, faction)

        #if characterData['race'] is Races.DWARF:
        #   characterData['strength'] = 4
        #   characterData['reflexes'] = 1
        #   characterData['perception'] = 2
        #   characterData['willpower'] = 4
        #   characterData['intelligence'] = 2
        #   characterData['charisma'] = 2
        #else:
        
        return newAgent