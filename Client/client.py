import json
import random

from websocket import WebSocket

import engine

class Client():
    _instance = None

    @staticmethod
    def Get():
        if Client._instance is None:
            Client._instance = Client()

        return Client._instance

    def __init__(self):
        self.socket = WebSocket()
        self.userId = random.randint(0, 65536)

    def Start(self):
        import configReader
        serverIp = configReader.ConfigReader.GetVariable('SERVER_IP')
        serverPort = configReader.ConfigReader.GetVariable('PORT')

        self.socket.connect('ws://' + serverIp + ':' + serverPort + '/')

        messageData = {'user_id' : self.userId}
        message = '[playerJoined, ' + json.dumps(messageData) + ']'
        self.socket.send(message)

        engine.Engine.Get().Start()

        self.Close()

    def GetMessage(self):
        messageData = self.socket.recv()
        return json.loads(messageData)

    def SendPlayerMovedMessage(self, factor):
        messageData = {'user_id' : self.userId, 'factor' : factor}
        message = '[playerMoved, ' + json.dumps(messageData) + ']'
        self.socket.send(message)

    def SendPlayerTurnedMessage(self, factor):
        messageData = {'user_id' : self.userId, 'factor' : factor}
        message = '[playerTurned, ' + json.dumps(messageData) + ']'
        self.socket.send(message)

    def SendPlayerFiredMessage(self):
        messageData = {'user_id' : self.userId}
        message = '[playerFired, ' + json.dumps(messageData) + ']'
        self.socket.send(message)

    def Close(self):
        self.socket.close()