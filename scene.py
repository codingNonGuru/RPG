class Scene:
    _scene = None

    @staticmethod
    def Get():
        if Scene._scene is None:
            Scene._scene = Scene()

        return Scene._scene

    def __init__(self):
        self.players = []
        self.missiles = []

    def Update(self):
        from engine import Engine
        deltaTime = Engine.Get().frameDelta

        for player in self.players:
            player.Update()

        for missile in self.missiles:
            missile.Update(deltaTime)

            if missile.IsDestroyable():
                self.missiles.remove(missile)