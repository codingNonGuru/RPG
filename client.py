import json
from websocket import WebSocket
import pygame
import random
import math

pygame.display.init()
screen = pygame.display.set_mode((800, 600), pygame.DOUBLEBUF)

socket = None

userId = random.randint(0, 65536)

def sendPlayerMovedMessage(direction):
    messageData = {'user_id' : userId, 'direction' : direction}
    message = '[playerMoved, ' + json.dumps(messageData) + ']'
    socket.send(message)

def sendPlayerFiredMessage():
    messageData = {'user_id' : userId}
    message = '[playerFired, ' + json.dumps(messageData) + ']'
    socket.send(message)

genericTriangle = [(10, 0), (-6, 6), (-6, -6)]

import configReader
serverIp = configReader.ConfigReader.GetVariable('SERVER_IP')
serverPort = configReader.ConfigReader.GetVariable('PORT')

while True:
    if socket is None:
        socket = WebSocket()
        socket.connect('ws://' + serverIp + ':' + serverPort + '/')

        messageData = {'user_id' : userId}
        message = '[playerJoined, ' + json.dumps(messageData) + ']'
        socket.send(message)

    pygame.event.pump()
    pressedKeys = pygame.key.get_pressed()

    if pressedKeys[pygame.K_ESCAPE]:
        pygame.quit()
        break

    if pressedKeys[pygame.K_w]:
        sendPlayerMovedMessage('forward')    
    elif pressedKeys[pygame.K_s]:
        sendPlayerMovedMessage('backwards')

    if pressedKeys[pygame.K_a]:
        sendPlayerMovedMessage('rightwards')
    elif pressedKeys[pygame.K_d]:
        sendPlayerMovedMessage('leftwards')

    if pressedKeys[pygame.K_SPACE]:
        sendPlayerFiredMessage()

    messageData = socket.recv()
    #print(messageData)
    message = json.loads(messageData)

    screen.fill((0, 0, 0))

    index = 0
    for position in message['positions']:
        rotation = message['rotations'][index]
        triangle = []
        for vertex in genericTriangle:
            x = vertex[0] * math.cos(rotation) - vertex[1] * math.sin(rotation)
            y = vertex[0] * math.sin(rotation) + vertex[1] * math.cos(rotation)
            triangle.append((x + position[0], y + position[1]))

        pygame.draw.polygon(screen, (255, 255, 255), triangle)
        index += 1

    for missile in message['missiles']:
        rotation = missile['rotation']
        position = (missile['x'], missile['y'])
        triangle = []
        for vertex in genericTriangle:
            x = vertex[0] * math.cos(rotation) - vertex[1] * math.sin(rotation)
            y = vertex[0] * math.sin(rotation) + vertex[1] * math.cos(rotation)
            x *= 0.5
            y *= 0.5
            triangle.append((x + position[0], y + position[1]))

        pygame.draw.polygon(screen, (255, 255, 255), triangle)

    pygame.display.flip()

socket.close()