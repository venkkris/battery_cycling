from galvani import BioLogic
import pandas as pd
import matplotlib.pyplot as plt

filename = '220218-PanasonicBR2032-90-100-C50_C14.mpr'
mpr_file = BioLogic.MPRfile(filename)
data = pd.DataFrame(mpr_file.data)


# Function to plot time series of voltage vs time
# Takes as input the pandas dataframe object
def plot_time_series(data, quantity, plot_name):
    plt.figure()
    plt.plot(data['time/s']/3600, data[quantity])
    plt.xlabel('Time (hr)')
    plt.ylabel(quantity)
    plt.savefig(plot_name)
    plt.show()


# Function to plot voltage vs capacity
# Takes as input the pandas dataframe object
def plot_voltage_capacity(data):
    plt.figure()
    plt.plot(-1*data['(Q-Qo)/mA.h'], data['Ewe/V'])
    plt.xlabel('Capacity (Ah)')
    plt.ylabel('Voltage (V)')
    plt.savefig('voltage_vs_capacity.png')
    plt.show()



# Preliminary data analysis
# print(data[0:20])


# Plots
plot_time_series(data, 'control/V/mA', 'control_ts.png')
# plot_voltage_capacity(data)



# Explanation of headers
# 'flags': No idea
# 'Ns': No idea
# 'time/s': Time in seconds
# 'dQ/mA.h': Change transferred in time step; essentially current
# '(Q-Qo)/mA.h': Capacity referenced to initial capacity
# 'control/V/mA': Control voltage or current
# 'Ewe/V': Voltage of the cell
# 'Q charge/discharge/mA.h': Capacity discharged or charged; resets to zero after switching cycles; negative for discharge
# 'half cycle': No idea; probably an index of when it switches from charging to discharging
