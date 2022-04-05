from Devices import *
import csv
import os
import serial
import time
from datetime import datetime
from itertools import count
from collections import defaultdict

hz = 1 # max is 16
debugging = True

allattr = 'VICPTHW'
Devices = {
    'SHTC3': 'TH',       # Temp Humidity
    'INA219': 'I',       # Current sensor across shunt
    'MAX31855': 'TC',    # Thermocouple Amplifier
    'MAX17043': 'VP',    # BFG
    'LC709203F': 'VPT',  # BFG
    'INA260': 'VIW'      # Current, Voltage, Power
}

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

def available_name(name:str, ext:str) -> str:
    prefix = '../data/'
    filename = f'{prefix}{name}.{ext}'
    if os.path.exists(filename):
        for i in count(1):
            if not os.path.exists(f'{prefix}{name}_{i}.{ext}'):
                filename = f'{prefix}{name}_{i}.{ext}'
                break
    return filename

def makeCSV(device:str, attr:str) -> str:
    # cols defaults to `attributes` dict above, but can be updated below
    cols = attributes.copy()
    updates = defaultdict(dict)
    updates.update(
        {
            'MAX31855':{'C':'Internal Temp (C)', 'T':'Thermocouple Temp (C)'}
        })
    cols.update(updates[device])

    # locate an available filename
    filename = available_name(device, 'csv')
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Device', *[cols[k] for k in attr], 'Timestamp'])
    debug(f'Created {filename}')
    return filename

def debug(msg:str):
    if debugging:
        print(msg)        

def main():
    sensors = {k: Sensor(k, v) for k, v in Devices.items()}

    # create a csv file for each sensor
    for k, v in sensors.items():
        sensors[k].filename = makeCSV(k, v.updstr)

    logfile = available_name('log','txt')
    with open(logfile, 'w') as log:
        log.write(f'Log started {datetime.now(timezone.utc)}\nLogging session with devices:\n')
        log.write('\n'.join([f'{str(v)} logging in file "{v.filename}"' for k, v in sensors.items()]))
        log.write('\n')

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
                    with open(logfile, 'a') as log:
                        log.write(f'[{datetime.now(timezone.utc)}] {s}: ' + recv['M'] + '\n')
                    if s == 'ERROR':
                        print(f'{s}: ' + recv['M'])
                        print('Exiting...')
                        return
                    debug(f'{s}: ' + recv['M'])
                    continue
                # if packet is a response, then add it to the set of responses
                # and update the sensor data, then print it to csv
                responses.add(s)
                sensors[s].update(recv)
                row = [s, *sensors[s].data(), str(datetime.now(timezone.utc))]
                with open(sensors[s].filename, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow(row)
                debug(','.join(row))
                
            # give serial time to fill again
            time.sleep(1/1000)
            
        # wait until the next packet should be sent
        if (time.time() - last_time) < 1/hz:
            debug(f'update took {time.time() - last_time} seconds')
            time.sleep(1/hz - (time.time() - last_time))
        else:
            print('LOG: overflow! cannot keep up with hz!')


if __name__ == '__main__':
    main()
