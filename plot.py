from galvani import BioLogic
import pandas as pd
import matplotlib.pyplot as plt
import cv2

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
#    plt.show()
    plt.close()


# Function to plot voltage vs capacity
# Takes as input the pandas dataframe object
def plot_voltage_capacity(data, plot_name, plot_title):
    plt.figure()
    plt.plot(-1*data['(Q-Qo)/mA.h'], data['Ewe/V'], '-*')
    plt.xlabel('Capacity (Ah)')
    plt.ylabel('Voltage (V)')
    plt.title(plot_title)
    plt.ylim(1.5, 4.8)
    plt.savefig(plot_name)
#    plt.show()
    plt.close()




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


# Plot cycling data
# Assumption: Always start with 1st discharge, then 1st charge
disch = 1
ch = 1
grouped = data.groupby("half cycle", sort=False)
disch_images = []
ch_images = []


for index in grouped.indices.keys():
    if grouped.get_group(index)['control/V/mA'].iloc[10] < 0:
        plot_voltage_capacity(grouped.get_group(index), 'cycles/discharge_' + str(disch) + '.png', plot_title=str(disch) + '$^{th}$ discharge')
        img = cv2.imread('cycles/discharge_' + str(disch) + '.png')
        height, width, layers = img.shape
        size = (width, height)
        disch_images.append(img)
        disch += 1
    else:
        plot_voltage_capacity(grouped.get_group(index), 'cycles/charge_' + str(ch) + '.png', plot_title=str(ch) + '$^{th}$ charge')
        img = cv2.imread('cycles/charge_' + str(ch) + '.png')
        ch_images.append(img)
        ch += 1

disch_video = cv2.VideoWriter('discharge.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 1, size)
ch_video = cv2.VideoWriter('charge.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 1, size)
for image in disch_images:
    disch_video.write(image)
for image in ch_images:
    ch_video.write(image)
disch_video.release()
ch_video.release()
