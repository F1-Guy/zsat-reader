from socket import *
import random

serverPort = 30000
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print(
    f'Server is ready to receive on port: {serverPort}')

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    print('Received message: ' + message.decode())

    # Server currently returns a random boolean
    # To be replaced with REST API call response
    modifiedMessage = str(bool(random.getrandbits(1)))
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)
