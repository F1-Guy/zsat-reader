from socket import *
import random
import json
import requests
from datetime import datetime

if __name__ == '__main__':
    with open('config.json') as f:
        data = json.load(f)

    serverPort = data.get('port', 50000)
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(('', serverPort))

    print(
        f'Server is ready to receive on port: {serverPort}')

    while True:
        message, clientAddress = serverSocket.recvfrom(2048)
        received = datetime.now()
        decoded_message = message.decode()
        print(f'At {received} received: {decoded_message}')

        # Server currently returns a random boolean
        # To be replaced with REST API call response
        response = str(bool(random.getrandbits(1)))

        serverSocket.sendto(response.encode(), clientAddress)
        sent = datetime.now()

        print(f'At {sent} sent: {response}\n')
