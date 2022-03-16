# Classes to connect to the individual Sensor devices

import serial, json
from time import sleep
from datetime import datetime, timezone

arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)

"""
V: volts (V)
I: current (A)
C: charged (mAh)
P: percentage
T: temperature (C)
"""

class Sensor(HID):
    # Generic class to interface with Sensor devices
    # this will provide a universal interface for data collecton between the three different Sensor devices
    def __init__(self):
        super().__init__()
        self.name = 'Generic Sensor device'
        self.manufacturer = 'generic'
        self.data = {s:'' for s in 'VICPT'}
        self.updstr = ''

    def data(self):
        if updstr == '':
            raise ValueError('No data in request string to be sent')
        arduino.write(
            bytes(f'{{{self.name}:{self.updstr}}}', encoding='utf-8'))
        time.sleep(0.05)
        self.data.update(
            json.load(str(arduino.readline(), encoding='utf-8')))
        return [self.name, *[self.data[key] for key in 'VICPT'], datetime.now(timezone.utc).__str__()]

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
