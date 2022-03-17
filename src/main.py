from Devices import *
import csv
import os
import serial
import time
from datetime import datetime

def main():

    Sensors = [Sensor()]

    for s in Sensors:
        header = ['Device', *[attributes[k] for k in s.updstr], 'Timestamp']
        print(','.join(header))
        start = time.time()
        print(','.join([s.name, *s.data(), datetime.now(timezone.utc).__str__()]))
        end = time.time()
        print(f"{s.name} took {end-start} seconds")
        # writer.writerow(s.data('VICPTHW'))
        time.sleep(0.05)

if __name__ == '__main__':
    main()
