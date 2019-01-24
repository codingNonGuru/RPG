import controller
import agent

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

        for i in range(0, 0):
            controllerData = {'isHuman' : False}
            newAgent = agent.Agent(controllerData, 'Los Chicos')
            
            self.agents.append(newAgent)

    def AddPlayer(self, id):
        controllerData = {'isHuman' : True, 'id' : id}
        newAgent = agent.Agent(controllerData, 'El Verdadero')
        
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