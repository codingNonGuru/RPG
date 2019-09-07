import time

class Engine:
    _engine = None

    @staticmethod
    def Get():
        if Engine._engine is None:
            Engine._engine = Engine()

        return Engine._engine

    def __init__(self):
        self.frameDelta = 0.0

    def Refresh(self):
        time.sleep(1.0)
        lastClock = time.clock()
        while True:
            time.sleep(0.033)

            self.frameDelta = time.clock() - lastClock
            self.frameDelta *= 100.0
            lastClock = time.clock()

            from scene import Scene
            Scene.Get().Update()

            from server import Server
            Server.Get().Broadcast()