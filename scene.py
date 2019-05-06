import controller
import agent
import agentFactory
from agentData import Attributes, Races, Classes
from vector import Vector
from spawnData import SpawnData

class Scene:
    _scene = None

    @staticmethod
    def Get():
        if Scene._scene is None:
            Scene._scene = Scene()

        return Scene._scene

    def __init__(self):
        self.agents = []
        self.missiles = []

        for i in range(0, 3):
            controllerData = {'isHuman' : False}
            characterData = {Attributes.CLASS : Classes.FIGHTER}
            spawnData = SpawnData(Vector(300.0, 200.0), 60.0)
            newAgent = agentFactory.AgentFactory.Get().GetAgent(controllerData, characterData, 'Los Chicos', spawnData)
            
            self.agents.append(newAgent)

    def AddPlayer(self, id):
        controllerData = {'isHuman' : True, 'id' : id}
        characterData = {Attributes.RACE : Races.DWARF, Attributes.CLASS : Classes.FIGHTER, Attributes.LEVEL : 1}
        newAgent = agent.Agent(Vector(0.0, 0.0), controllerData, characterData, 'El Verdadero')
        
        self.agents.append(newAgent)

    def Update(self):
        from engine import Engine
        deltaTime = Engine.Get().frameDelta

        for agent in self.agents:
            for missile in self.missiles:
                if agent.CheckCollision(missile):
                    missile.Damage()
                    agent.Damage()

        for agent in self.agents:
            agent.Update()

        for missile in self.missiles:
            missile.Update(deltaTime)

            if missile.IsDestroyable():
                self.missiles.remove(missile)