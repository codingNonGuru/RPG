import agent
from agentData import Races

class AgentFactory():
    _instance = None

    @staticmethod
    def Get():
        if AgentFactory._instance is None:
            AgentFactory._instance = AgentFactory()

        return AgentFactory._instance

    def GetAgent(self, controllerData, characterData, faction):
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