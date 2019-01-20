class Controller(object):
    def __init__(self):
        self.isMoving = False
        self.isTurning = False
        self.isShooting = False
        self.moveDirection = None
        self.turnDirection = None

class HumanController(Controller):
    def __init__(self, id):
        super(HumanController, self).__init__()   
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

    def Reset(self):
        self.isMoving = False
        self.isTurning = False
        self.isShooting = False

class MachineController(Controller):
    def __init__(self):
        super(MachineController, self).__init__()