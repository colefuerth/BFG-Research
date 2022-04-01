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
#     'INA260': 'VIW'      # Current, Voltage, Power
#     'INA219': 'I',       # Current sensor across shunt
# }

allattr = 'VICPTHW'
Devices = {
    'SHTC3': 'TH',       # Temp Humidity
    'MAX31855': 'C'    # Thermocouple Amplifier
}

def main():
    sensors = {k: Sensor(k, v) for k, v in Devices.items()}
    hz = 2

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
                # get response key
                s = recv['D']
                # if packet is a log, then print it
                if s in ['LOG', 'ERROR']:
                    print(f'{s}: ' + recv['M'])
                    if s == 'ERROR':
                        print('Exiting...')
                        return
                    continue
                # if packet is a response, then add it to the set of responses
                # and update the sensor data, then print it to csv
                responses.add(s)
                sensors[s].update(recv)
                print(','.join([s, *sensors[s].data(), str(datetime.now(timezone.utc))]), end='\n\n')
            # give serial time to fill again
            time.sleep(1/1000)
            
        # wait until the next packet should be sent
        if (time.time() - last_time) < 1/hz:
            time.sleep(1/hz - (time.time() - last_time))
        else:
            print('LOG: overflow! cannot keep up with hz!')


if __name__ == '__main__':
    main()
