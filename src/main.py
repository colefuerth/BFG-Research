from Devices import *
import csv
import os
import serial
import time
from datetime import datetime
from itertools import count

# Devices = {
#     'LC709203F': 'VPT',  # BFG
#     'LTC2941': 'CP',     # BFG
#     'MAX17043': 'VP',    # BFG
#     'SHTC3': 'TH',       # Temp Humidity
#     'MAX31855': 'C',     # Thermocouple Amplifier
#     'INA260': 'VIW'      # Current, Voltage, Power
#     'INA219': 'I',       # Current sensor across shunt
# }

allattr = 'VICPTHW'
Devices = {
    "none": allattr,
    "MAX17043": allattr  # BFG
}

def main():
    sensors = {k: Sensor(k, v) for k, v in Devices.items()}
    hz = 1

    # NOTE: this is temporary to test all attributes on all devices
    header = ['Device', *[attributes[k] for k in allattr], 'Timestamp']
    print(','.join(header))

    while(True):
        # send a request packet with all sensors in it
        sendpayload(sensors)

        # record last time sent, so we know when to send a new packet
        last_time = time.time()

        # wait for all response packets to be received
        responses = set()
        while responses != set(sensors.keys()):
            # need to recv packet and then process it
            recv = recvpayload()
            if recv:
                # update the sensor
                # print(recv)
                s = recv['D']
                if s == 'LOG':
                    print('LOG: ' + recv['M'])
                    continue
                responses.add(s)
                sensors[s].update(recv)
                print(','.join([s, *sensors[s].data(), datetime.now(timezone.utc).__str__()]))
            time.sleep(5/1000)
            
        # wait until the next packet should be sent
        if (time.time() - last_time) < 1/hz:
            time.sleep(1/hz - (time.time() - last_time))


if __name__ == '__main__':
    main()
