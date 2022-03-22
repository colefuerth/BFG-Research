from Devices import *
import csv
import os
import serial
import time
from datetime import datetime
from itertools import count

Devices = {
    'LC709203F': 'VPT',  # BFG
    'LTC2941': 'CP',     # BFG
    'MAX17043': 'VP',    # BFG
    'SHTC3': 'TH',       # Temp Humidity
    'MAX31855': 'C',     # Thermocouple Amplifier
    'INA260': 'VIW'      # Current, Voltage, Power
}

def main():
    sensors = {k: Sensor(k, v) for k, v in Devices.items()}
    hz = 5

    header = ['Device', *[attributes[k] for k in s.updstr], 'Timestamp']
    print(','.join(header))
    sendpayload(sensors)
    c = count(0)
    while next(c) < len(sensors):
        # need to recv packet and then process it
        print(','.join([s.name, *s.data(), datetime.now(timezone.utc).__str__()]))
        # writer.writerow(s.data('VICPTHW'))
        time.sleep(1/hz)


if __name__ == '__main__':
    main()
