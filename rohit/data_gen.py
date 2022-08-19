# %% [markdown]
# # Synchronize Timestamps across multiple CSV files
# 
# - truncate leading and trailing timestamps
# - uses the lowest resolution timestamp interval from all the CSV files
# - for each point at the lowest resolution, find the nearest point in each CSV file and collect them into a new CSV file

# %%
import pandas as pd
import datetime


# %%
# create a dict of the dataframes
dfnames = {
    'LC709203F': pd.read_csv("LC709203F_5.csv"),
    'MAX17043' : pd.read_csv("MAX17043_5.csv"),
    'Arbin'    : pd.read_csv('BFG_take_2_Channel_2_Wb_1.CSV'),
    'INA219'   : pd.read_csv('INA219_5.csv'),
    'SHTC3'    : pd.read_csv('SHTC3_5.csv')
}


# %%
# Prepare Arbin data for comparison with other data

# rename relevant columns for comparing to dfnames['BFG1'] and dfnames['BFG2']
dfnames['Arbin'] = dfnames['Arbin'].rename(
    columns={'Date_Time': 'Timestamp'})
# convert the timestamps to datetime objects
for name, df in dfnames.items():
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
# convert arbin timestamps from EST (-4 at time of recording) to UTC (0)
dfnames['Arbin']['Timestamp'] = (dfnames['Arbin']['Timestamp'] +
                                 datetime.timedelta(hours=4)).dt.tz_localize('UTC')
# add decimal seconds to arbin timestamps (arbin timestamps are in whole seconds, but recorded at 2hz)
dfnames['Arbin']['Test_Time(s)'] = dfnames['Arbin']['Test_Time(s)'].astype(
    float) % 1
dfnames['Arbin']['Timestamp'] = dfnames['Arbin']['Timestamp'] + \
    pd.to_timedelta(dfnames['Arbin']['Test_Time(s)'], unit='s')


# %%
# truncate database entries that have timestamps that are leading or trailing

# drop datapoints that are outside of the range of the timestamps
first = max([df['Timestamp'].iat[0] for df in dfnames.values()])
last = min([df['Timestamp'].iat[-1] for df in dfnames.values()])
for name, df in dfnames.items():
    df = df.drop(df[(df.Timestamp < first) | (df.Timestamp > last)].index)
    df = df.reset_index(drop=True)
    dfnames[name] = df


# %%
# create the output dataset and fill it with data that can be directly compared to the Arbin data

output_df = pd.DataFrame()

# reuse the timestamp column with the lowest resolution column
output_df['Timestamp'] = max(
    dfnames.values(), key=lambda x: x.Timestamp.diff().mean())['Timestamp']


# %%
# convert timestamps to floating values relative to an epoch

epoch = output_df['Timestamp'].iat[0]
output_df['Timestamp'] = (output_df['Timestamp'] - epoch).dt.total_seconds()
# round output timestamps to the nearest ms
output_df['Timestamp'] = output_df['Timestamp'].round(3)
for name, df in dfnames.items():
    df['Timestamp'] = (df['Timestamp'] - epoch).dt.total_seconds()


# %%
# define a function for moving columns from one dataframe to another and aligning timestamps

def align_timestamps(output_df: pd.DataFrame, input_df: pd.DataFrame, column_map: dict):
    """
    align timestamps in the input_df onto timestamps in output_df, copy columns using the column_map

    parameters:
    output_df: the dataframe being copied into
    input_df: the dataframe being copied from
    column_map: a dict mapping input_df columns to output_df columns
    """
    indices = input_df['Timestamp'].searchsorted(output_df['Timestamp']) - 1
    for col, out_col in column_map.items():
        output_df[out_col] = pd.Series([input_df[col].iat[i] for i in indices])


# %%
# copy columns from each source df into the output df

align_timestamps(output_df, dfnames['Arbin'], {
                 col: col + '_Arbin' for col in 'Current(A),Voltage(V),Power(W),Charge_Capacity(Ah),Discharge_Capacity(Ah),Charge_Energy(Wh),Discharge_Energy(Wh)'.split(',')})
align_timestamps(output_df, dfnames['LC709203F'], {
                 'Voltage': 'Voltage(V)_LC709203F', 'Percentage': 'SOC(%)_LC709203F'})
align_timestamps(output_df, dfnames['MAX17043'], {
                 'Voltage': 'Voltage(V)_MAX17043', 'Percentage': 'SOC(%)_MAX17043'})
align_timestamps(output_df, dfnames['INA219'], {
                 'Current (mA)': 'Current (mA)_INA219'})
align_timestamps(output_df, dfnames['SHTC3'], {
                 header: header + '_SHTC3' for header in 'Temperature (C),Humidity'.split(',')})


# %%
# save the output dataset
output_df.to_csv('output.csv', index=False)


