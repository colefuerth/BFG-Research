from Devices import *
import csv
import os

def main():
    # print(f"Logging to CSV file {os.argv[1]}")

    Sensors = [Sensor()]
    header = ['Device', 'Voltage (V)', 'Current (A)', 'Charged (mAh)', 'Percentage', 'Temperature (C)', 'Humidity', 'Power (W)', 'Timestamp']

    # with open(os.argv[1], 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile, delimiter=',')
    #     writer.writerow()

    print(','.join(header))

    for s in Sensors:
        print(','.join(s.data()))
        # writer.writerow(s.data('VICPTHW'))
        time.sleep(0.05)

if __name__ == '__main__':
    main()