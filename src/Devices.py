# Classes to connect to the individual Sensor devices

import serial
import json
from time import sleep
from datetime import datetime, timezone

arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.05)

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
    def __init__(name, updstr):
        self.name = name
        self.updstr = updstr
        self.datadict = {s: '' for s in self.updstr}

    def data(self):
        sent = f'{{"{self.name}":"{self.updstr}"}}'
        arduino.write(sent.encode('utf-8'))
        arduino.flush()
        while arduino.inWaiting() == 0:
            print('.', end='')
            sleep(.01)
        recv = arduino.readline().decode('utf-8')
        recv = json.loads(recv)
        assert(recv["D"] == self.name)
        self.datadict.update(recv)
        return [self.datadict[key] for key in self.updstr]

    def __str__(self):
        return f'{self.name}:{self.updstr}'


# class LC709203F(Sensor):
#     # Specific class for Sensor-1
#     def __init__(self):
#         super().__init__()
#         self.name = 'LC709203F'
#         self.manufacturer = 'AdaFruit'
#         self.updstr = 'VPT'


# class LTC2941(Sensor):
#     # Specific class for Sensor-2
#     def __init__(self):
#         super().__init__()
#         self.name = 'LTC2941'
#         self.manufacturer = 'Analog Device'
#         self.updstr = 'CP'


# class MAX17043(Sensor):
#     # Specific class for Sensor-3
#     def __init__(self):
#         super().__init__()
#         self.name = 'MAX17043'
#         self.manufacturer = 'Maxim Integrated'
#         self.updstr = 'VP'
