# Classes to connect to the individual Sensor devices

import serial
import json
from time import sleep
from datetime import datetime, timezone

arduino = serial.Serial(port='COM5', baudrate=9600, timeout=.5)

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
    def __init__(self):
        self.name = 'none'
        self.manufacturer = 'generic'
        self.datadict = {s: '' for s in attributes.keys()}
        self.updstr = ''.join(attributes.keys())

    def data(self):
        sent = f'{{"{self.name}":"{self.updstr}"}}'
        print('sent: ' + sent)
        arduino.write(
            bytes(sent, encoding='utf-8'))
        sleep(0.1)
        recv = arduino.readline()
        print(recv)
        recv = str(arduino.readline(), encoding='utf-8')
        print('recv: ' + recv)
        recv = json.load(recv)
        assert(recv["D"] == self.updstr)
        recv.pop('D')
        self.datadict.update(recv)
        return [self.name, *[self.datadict[key] for key in updstr], datetime.now(timezone.utc).__str__()]

    def __str__(self):
        return f'{self.name} ({self.manufacturer})'


class LC709203F(Sensor):
    # Specific class for Sensor-1
    def __init__(self):
        super().__init__()
        self.name = 'LC709203F'
        self.manufacturer = 'AdaFruit'
        self.updstr = 'VPT'


class LTC2941(Sensor):
    # Specific class for Sensor-2
    def __init__(self):
        super().__init__()
        self.name = 'LTC2941'
        self.manufacturer = 'Analog Device'
        self.updstr = 'CP'


class MAX17043(Sensor):
    # Specific class for Sensor-3
    def __init__(self):
        super().__init__()
        self.name = 'MAX17043'
        self.manufacturer = 'Maxim Integrated'
        self.updstr = 'VP'
