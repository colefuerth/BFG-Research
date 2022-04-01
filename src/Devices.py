# Classes to connect to the individual Sensor devices

import serial
import json
from time import sleep
from datetime import datetime, timezone

arduino = serial.Serial(port='COM5', baudrate=115200, timeout=.05)  

# callable attributes on sensors
attributes = {
    'V': 'Voltage',
    'I': 'Current (mA)',
    'C': 'Charge (mAh)',
    'P': 'Percentage',
    'T': 'Temperature (C)',
    'H': 'Humidity',
    'W': 'Power (W)',
}


class Sensor:
    # Generic class to interface with Sensor devices
    # this will provide a universal interface for data collecton between the three different Sensor devices
    def __init__(self, name, updstr):
        self.name = name
        self.updstr = updstr
        self.datadict = {s: '' for s in self.updstr}

    def update(self, data:dict) -> None:
        assert(data["D"] == self.name)
        self.datadict.update(data)

    def data(self) -> list:
        return [self.datadict[key] for key in self.updstr]

    def __str__(self) -> str:
        return f'"{self.name}":"{self.updstr}"'


# accepts both a sensor, or a dict of sensors
def sendpayload(request) -> None:
    if arduino is None:
        print('arduino not initialized')
        return
    msg = "{"
    if isinstance(request, dict):
        msg += ','.join([str(v) for v in request.values()])
    else:
        msg += str(request)
    msg += "}"
    print(msg)
    arduino.write(msg.encode('utf-8'))
    arduino.flush()

def recvpayload() -> dict:
    if arduino is None:
        print('arduino not initialized')
        return
    if arduino.inWaiting() == 0:
        return None
    recv = arduino.readline().decode('utf-8').strip()
    print(recv)
    recv = json.loads(recv)
    return recv