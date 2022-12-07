import json
import requests
from socket import *
from datetime import datetime


def Server():
    while True:
        message, client_address = server_socket.recvfrom(2048)
        received = datetime.now()
        decoded_message = message.decode()

        payload = json.loads(decoded_message)
        print(f'At {received} received and decoded: {decoded_message}')

        request_url = f'{api_url}?cardId={payload["card_id"]}&timestamp={payload["timestamp"]}&lessonId={payload["lesson_id"]}'
        request = requests.post(request_url)

        if request.status_code == 201:
            response = 'Success'
        else:
            response = 'Failure'

        server_socket.sendto(response.encode(), client_address)
        sent = datetime.now()

        print(f'At {sent} sent: {response}\n')


if __name__ == '__main__':
    with open('config.json') as f:
        data = json.load(f)

    serverPort = data.get('port', 0)
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind(('', serverPort))
    api_url = data.get('api_url', 'NOT SET')

    print(f'Server is ready to receive on port: {serverPort}')
    print(f'API ebdpoint is: {api_url}')

    Server()
