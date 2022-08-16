# import CSVs into pandas and display charts
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

# clc;
# clear all;

# BFG_1 = xlsread("LC709203F_5.csv");
BFG1 = pd.read_csv("LC709203F_5.csv")
# BFG_2 = xlsread("MAX17043_5.csv");
BFG2 = pd.read_csv("MAX17043_5.csv")


# BFG_arbin = xlsread('BFG_take_2_Channel_2_Wb_1.CSV');
BFG_arbin = pd.read_csv('BFG_take_2_Channel_2_Wb_1.CSV')

# convert the timestamps to datetime objects
BFG1['Timestamp'] = pd.to_datetime(BFG1['Timestamp'])
BFG2['Timestamp'] = pd.to_datetime(BFG2['Timestamp'])
BFG_arbin['Date_Time'] = pd.to_datetime(BFG_arbin['Date_Time'])
# convert arbin timestamps from EST (-4) to UTC (0)
BFG_arbin['Date_Time'] = BFG_arbin['Date_Time'] + datetime.timedelta(hours=4)
# mark the timezone on arbin as UTC (now that we applied the offset)
BFG_arbin['Date_Time'] = BFG_arbin['Date_Time'].dt.tz_localize('UTC')

# find the first datapoint on the BFGs that occurs AFTER beginning the Arbin data collection
front = 0
for entry in BFG1['Timestamp']:
    if entry < BFG_arbin['Date_Time'][0]:
        front += 1
    else:
        break
# find the first datapoint on the BFGs that occurs AFTER completing the Arbin data collection (commented out because rohit does not want to drop the back points, but this is how we find that point)
# back = 0
# for entry in reversed(BFG1['Timestamp']):
#     if entry > BFG_arbin['Date_Time'].iat[-1]:
#         back += 1
#     else:
#         break

# drop rows from the beginning and end of the data that do not line up (rohit says do not drop the back points)
# add `-back` to 'front:' to drop the back points
BFG1 = BFG1.iloc[front:, :]
BFG2 = BFG2.iloc[front:, :]

# print the beginning and ends of each table, to show that timestamps line up now
# print(BFG1['Timestamp'])
# print(BFG2['Timestamp'])
# print(BFG_arbin['Date_Time'])

# get relevant columns from the tables

# BFG_ar_cur = BFG_arbin(:,7);
BFG_ar_cur = BFG_arbin['Current(A)']
# BFG_ar_vol = BFG_arbin((244:end),8);
BFG_ar_vol = BFG_arbin['Voltage(V)']#[243:]
BFG_ar_time = BFG_arbin['Date_Time']

# BFG_1_vol = BFG_1((335:end),1);
BFG_1_vol = BFG1['Voltage']#[334:]
# BFG_2_vol = BFG_2((337:end),1);
BFG_2_vol = BFG2['Voltage']#[336:]
BFG_1_2_time = BFG1['Timestamp']

# plot the data

# h =figure;

# plot(BFG_1_vol,LineWidth=1.5);
# plot BFG_1
plt.plot(BFG_1_2_time, BFG_1_vol, label='BFG_1')
# hold on;
# plot(BFG_2_vol,LineWidth=1.5);
# plot BFG_2
plt.plot(BFG_1_2_time, BFG_2_vol, label='BFG_2')
# legend('BFG_1 (Adafruit)','BFG_2 (Maximum Integrated)','Arbin');
# plot(BFG_ar_vol,LineWidth=1.5);
# plot arbin
plt.plot(BFG_ar_time, BFG_ar_vol, label='Arbin')
# title('Voltage Comparison');
plt.legend(['BFG_1 (Adafruit)', 'BFG_2 (Maximum Integrated)', 'Arbin'])
plt.title('Voltage Comparison')

# display the plot
plt.show()
