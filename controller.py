import math

import scene

class Controller(object):
    def __init__(self, parent):
        self.isMoving = False
        self.isTurning = False
        self.isShooting = False
        self.moveDirection = None
        self.turnDirection = None
        self.target = None
        self.parent = parent

    def Reset(self):
        self.isMoving = False
        self.isTurning = False
        self.isShooting = False

class HumanController(Controller):
    def __init__(self, parent, id):
        super(HumanController, self).__init__(parent)   
        self.id = id

    def Update(self):
        self.Reset()

        from server import Server
        for event in Server.Get().events:
            if event.data['user_id'] != self.id:
                continue

            if event.name == 'move':
                direction = event.data['direction']

                if direction == 'forward' or direction == 'backwards':
                    self.isMoving = True
                    self.moveDirection = direction
                else:
                    self.isTurning = True
                    self.turnDirection = direction
            elif event.name == 'fire':
                self.isShooting = True

            Server.Get().events.remove(event)

class MachineController(Controller):
    def __init__(self, parent):
        super(MachineController, self).__init__(parent)

    def Update(self):
        self.Reset()

        closestAgent = None
        closestDistance = 9999.0
        for agent in scene.Scene.Get().agents:
            if agent is self.parent:
                continue

            x = self.parent.x - agent.x
            y = self.parent.y - agent.y
            distance = math.sqrt(x * x + y * y)

            if distance < closestDistance:
                closestDistance = distance
                closestAgent = agent

        self.target = closestAgent