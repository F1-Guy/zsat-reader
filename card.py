from socket import *
import evdev
import time
from datetime import datetime
from evdev import categorize, ecodes
from sense_hat import SenseHat
import json

# Sense Hat setup
s = SenseHat()
green = (0, 255, 0)
red = (255, 0, 0)
nothing = (0, 0, 0)

# Sense Hat display setup


def green_check():
    G = green
    O = nothing
    logo = [
        O, O, O, O, O, O, O, O,
        O, O, O, O, O, O, O, G,
        O, O, O, O, O, O, G, O,
        O, O, O, O, O, G, O, O,
        G, O, O, O, G, O, O, O,
        O, G, O, G, O, O, O, O,
        O, O, G, O, O, O, O, O,
        O, O, O, O, O, O, O, O,
    ]
    return logo


def red_x():
    R = red
    O = nothing
    logo = [
        R, O, O, O, O, O, O, R,
        O, R, O, O, O, O, R, O,
        O, O, R, O, O, R, O, O,
        O, O, O, R, R, O, O, O,
        O, O, O, R, R, O, O, O,
        O, O, R, O, O, R, O, O,
        O, R, O, O, O, O, R, O,
        R, O, O, O, O, O, O, R,
    ]
    return logo


def red_q():
    R = red
    O = nothing
    logo = [
        O, O, O, R, O, O, O, O,
        O, O, R, O, R, O, O, O,
        O, O, R, O, R, O, O, O,
        O, O, O, O, R, O, O, O,
        O, O, O, O, R, O, O, O,
        O, O, O, R, O, O, O, O,
        O, O, O, O, O, O, O, O,
        O, O, O, R, O, O, O, O,
    ]
    return logo


class Device():
    name = 'Sycreader RFID Technology Co., Ltd SYC ID&IC USB Reader'

    @classmethod
    def list(cls, show_all=False):
        devices = [evdev.InputDevice(fn) for fn in evdev.list_devices()]
        if show_all:
            for device in devices:
                print("event: " + device.fn, "name: " +
                      device.name, "hardware: " + device.phys)
        return devices

    @classmethod
    def connect(cls):
        try:
            device = [dev for dev in cls.list() if cls.name in dev.name][0]
            device = evdev.InputDevice(device.fn)
            return device
        except IndexError:
            print("Device not found.\n - Check if it is properly connected. \n - Check permission of /dev/input/ (see README.md)")
            exit()

    @classmethod
    def run(cls):
        device = cls.connect()
        container = []

        try:
            device.grab()
            print("RFID scanner is ready....")

            for event in device.read_loop():
                if event.type == ecodes.EV_KEY and event.value == 1:
                    digit = evdev.ecodes.KEY[event.code]
                    if digit == 'KEY_ENTER':
                        # create and dump the tag
                        tag = "".join(i.strip('KEY_') for i in container)

                        message = tag

                        client_socket.sendto(
                            message.encode(), (server_name, server_port))
                        sent = datetime.now()

                        modified_message, server_address = client_socket.recvfrom(
                            2048)
                        received = datetime.now()

                        decoded_message = modified_message.decode()

                        print(
                            f'At {sent} sent: {message}\nAt {received} received: {decoded_message}\n')

                        if decoded_message == 'True':
                            s.set_pixels(green_check())
                        elif decoded_message == 'False':
                            s.set_pixels(red_x())
                        else:
                            s.set_pixels(red_q())
                            print("Error")

                        container = []

                        time.sleep(1)
                        s.clear(0, 0, 0)

                    else:
                        container.append(digit)

        except:
            device.ungrab()
            print('WARNING: Qutting with exception')


if __name__ == '__main__':
    print("Don't forget to change the server IP and port in config.json")

    with open('config.json') as f:
        data = json.load(f)

    # UDP server info
    server_name = data.get('server_name', 'localhost')
    server_port = data.get('port', 50000)

    print(f'Connecting the server: {server_name}')
    print(f'Server port is: {server_port}')

    client_socket = socket(AF_INET, SOCK_DGRAM)
    client_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

    Device.run()
