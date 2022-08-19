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
BFG1 = pd.read_csv("LC709203F_5.csv")
BFG2 = pd.read_csv("MAX17043_5.csv")
BFG_arbin = pd.read_csv('BFG_take_2_Channel_2_Wb_1.CSV')


# %%
# convert the timestamps to datetime objects
BFG1['Timestamp'] = pd.to_datetime(BFG1['Timestamp'])
BFG2['Timestamp'] = pd.to_datetime(BFG2['Timestamp'])
BFG_arbin['Date_Time'] = pd.to_datetime(BFG_arbin['Date_Time'])
# convert arbin timestamps from EST (-4 at time of recording) to UTC (0)
if BFG_arbin['Date_Time'].iat[0].tzinfo is None:
    BFG_arbin['Date_Time'] = BFG_arbin['Date_Time'] + \
        datetime.timedelta(hours=4)
    BFG_arbin['Date_Time'] = BFG_arbin['Date_Time'].dt.tz_localize('UTC')
# add decimal seconds to arbin timestamps (arbin timestamps are in whole seconds, but recorded at 2hz)
BFG_arbin['Test_Time(s)'] = BFG_arbin['Test_Time(s)'].astype(float) % 1
BFG_arbin['Date_Time'] = BFG_arbin['Date_Time'] + \
    pd.to_timedelta(BFG_arbin['Test_Time(s)'], unit='s')

# rename relevant columns for comparing to BFG1 and BFG2
BFG_arbin = BFG_arbin.rename(
    columns={'Date_Time': 'Timestamp'})

# create a dict of the dataframes
dfnames = {'LC709203F': BFG1, 'MAX17043': BFG2, 'Arbin': BFG_arbin}
del BFG1, BFG2, BFG_arbin

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

# start with grabbing anything remotely useful from Arbin
arbin_cols = 'Current(A),Voltage(V),Power(W),Charge_Capacity(Ah),Discharge_Capacity(Ah),Charge_Energy(Wh),Discharge_Energy(Wh)'.split(',')
for col in arbin_cols:
    align_timestamps(output_df, dfnames['Arbin'], {col: col + '_Arbin'})

# copy columns from LC709203F and MAX17043
align_timestamps(output_df, dfnames['LC709203F'], {
                 'Voltage': 'Voltage(V)_LC709203F', 'Percentage': 'SOC(%)_MAX17043'})
align_timestamps(output_df, dfnames['MAX17043'], {
                 'Voltage': 'Voltage(V)_MAX17043', 'Percentage': 'SOC(%)_MAX17043'})


# %%
# save the output dataset
output_df.to_csv('output.csv', index=False)


