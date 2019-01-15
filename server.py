import json
import random
import re
import math

from websocket_server import WebsocketServer

from scene import Scene

class Server:
    _server = None

    @staticmethod
    def Get():
        if Server._server is None:
            Server._server = Server()

        return Server._server

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 8787
        self.server = WebsocketServer(self.port, self.host)
        self.server.set_fn_message_received(Server.handleMessage)

    @staticmethod
    def handlePlayerJoined(message):
        import player

        id = message['user_id']
        newPlayer = player.Player(id)
        Scene.Get().players.append(newPlayer)

    @staticmethod
    def handlePlayerMoved(message):
        id = message['user_id']
        direction = message['direction']
        for player in Scene.Get().players:
            if player.id == id:
                if direction == 'rightwards':
                    player.rotation -= 0.02
                elif direction == 'leftwards':
                    player.rotation += 0.02

                if 'forward' == direction:
                    player.x += math.cos(player.rotation)
                    player.y += math.sin(player.rotation)
                elif 'backwards' == direction:
                    player.x -= math.cos(player.rotation)
                    player.y -= math.sin(player.rotation)
                break

    @staticmethod
    def handlePlayerFired(message):
        id = message['user_id']
        for player in Scene.Get().players:
            if player.id == id:
                player.Fire()
                break

    @staticmethod
    def handleMessage(client, server, message):
        regex = "\[(.*), {(.*)}\]"
        searchResult = re.search(regex, message)

        messageType = searchResult.group(1)
        messageData = '{' + searchResult.group(2) + '}'

        message = json.loads(messageData)

        if "playerJoined" == messageType:
            Server.handlePlayerJoined(message)
        elif "playerMoved" == messageType:
            Server.handlePlayerMoved(message)
        elif "playerFired" == messageType:
            Server.handlePlayerFired(message)

    def Broadcast(self):
        eventObject = {'positions' : [], 'rotations' : [], 'missiles' : []}

        for player in Scene.Get().players:
            eventObject['positions'].append((player.x, player.y))
            eventObject['rotations'].append(player.rotation)

        for missile in Scene.Get().missiles:
            missileData = {'x' : missile.x, 'y' : missile.y, 'rotation' : missile.rotation}
            eventObject['missiles'].append(missileData)

        eventData = json.dumps(eventObject)

        self.server.send_message_to_all(eventData)

    def Start(self):
        self.server.run_forever()