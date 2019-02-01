import json
import random
import re
import math

from websocket_server import WebsocketServer

from scene import Scene
from event import Event
from agentData import Attributes

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
        self.server.set_fn_client_left(Server.handleConnected)
        self.server.set_fn_message_received(Server.handleMessage)
        self.events = []

    @staticmethod
    def handleConnected(client, server):
        print('AMEDEO')

    @staticmethod
    def handlePlayerJoined(message):
        id = message['user_id']
        Scene.Get().AddPlayer(id)

    @staticmethod
    def handlePlayerMoved(message):
        event = Event('move', message)
        Server.Get().events.append(event)

    @staticmethod
    def handlePlayerTurned(message):
        event = Event('turn', message)
        Server.Get().events.append(event)

    @staticmethod
    def handlePlayerFired(message):
        event = Event('fire', message)
        Server.Get().events.append(event)

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
        elif "playerTurned" == messageType:
            Server.handlePlayerTurned(message)
        elif "playerFired" == messageType:
            Server.handlePlayerFired(message)

    def Broadcast(self):
        eventObject = {'missiles' : [], 'agents' : []}

        for agent in Scene.Get().agents:
            agentData = {
                'position' : (agent.position.x, agent.position.y), 
                'rotation' : agent.rotation, 
                'hitpoints' : agent.hitpointCount,
                Attributes.RACE : agent.characterData[Attributes.RACE],
                Attributes.CLASS : agent.characterData[Attributes.CLASS],
                Attributes.LEVEL : agent.characterData[Attributes.LEVEL]
                }
            eventObject['agents'].append(agentData)            

        for missile in Scene.Get().missiles:
            missileData = {'x' : missile.position.x, 'y' : missile.position.y, 'rotation' : missile.rotation}
            eventObject['missiles'].append(missileData)

        eventData = json.dumps(eventObject)

        self.server.send_message_to_all(eventData)

    def Start(self):
        self.server.run_forever()