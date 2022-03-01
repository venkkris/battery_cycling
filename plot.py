from galvani import BioLogic
import pandas as pd
import matplotlib.pyplot as plt

filename = '220218-PanasonicBR2032-90-100-C50_C14.mpr'
mpr_file = BioLogic.MPRfile(filename)
data = pd.DataFrame(mpr_file.data)


# Function to plot time series of voltage vs time
# Takes as input the pandas dataframe object
def plot_time_series(data):
    plt.figure()
    plt.plot(data['time/s']/3600, data['Ewe/V'])
    plt.xlabel('Time (hr)')
    plt.ylabel('Voltage (V)')
    # plt.savefig('time_series.png')
    plt.show()


# Function to plot voltage vs capacity
# Takes as input the pandas dataframe object
def plot_voltage_capacity(data):
    plt.figure()
    plt.plot(-1*data['(Q-Qo)/mA.h'], data['Ewe/V'])
    plt.xlabel('Capacity (Ah)')
    plt.ylabel('Voltage (V)')
    # plt.savefig('voltage_capacity.png')
    plt.show()


# Function to plot voltage vs dq
# Takes as input the pandas dataframe object
def plot_time_series_half_cycle(data):
    plt.figure()
    plt.plot(data['time/s'], data['half cycle'])
    plt.xlabel('time')
    plt.ylabel('half cycle')
    # plt.savefig('voltage_dq.png')
    plt.show()


# Preliminary data analysis
# print(data.axes)
print(data)


# Plots
# plot_time_series(data)
# plot_voltage_capacity(data)
plot_time_series_half_cycle(data)
print(data['half cycle'])
