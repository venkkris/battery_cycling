from galvani import BioLogic
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import cv2
import numpy as np

# Convert .mpr file into a Pandas dataframe
filename = '220218-PanasonicBR2032-90-100-C50_C14.mpr'
mpr_file = BioLogic.MPRfile(filename)
data = pd.DataFrame(mpr_file.data)

def colorFader(c1,c2,mix=0): #fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)

# Function to plot time series of voltage vs time
# Takes as input the pandas dataframe object, quantity to be plotted on y axis, plot name
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
#    plt.plot(-1*data['(Q-Qo)/mA.h'], data['Ewe/V'], '-*')
    plt.plot(-1*data['Q charge/discharge/mA.h'], data['Ewe/V'], '-o')
    plt.xlabel('Capacity (mAh)')
    plt.ylabel('Voltage (V)')
    plt.title(plot_title)
    plt.ylim(1.5, 4.8)
    plt.savefig(plot_name)
#    plt.show()
    plt.close()



# Plot cycling data
# Assumption: Always start with 1st discharge, then 1st charge
disch = 1           # Index
ch = 1              # Index
disch_images = []   # Array of discharge images
ch_images = []      # Array of charge images
color1 = 'red'
color2 = 'black'


# Split into groups based on half cycles
grouped = data.groupby("half cycle", sort=False)

# Plot each charge and discharge cycle as separate plot
for index in grouped.indices.keys():

    # If discharge i.e. current is negative
    if grouped.get_group(index)['control/V/mA'].iloc[10] < 0:
        data = grouped.get_group(index)
        plot_voltage_capacity(data=grouped.get_group(index), 
        plot_name='cycles/discharge_' + str(disch) + '.png', 
        plot_title=str(disch) + '$^{th}$ discharge')

        img = cv2.imread('cycles/discharge_' + str(disch) + '.png')
        height, width, layers = img.shape
        size = (width, height)
        disch_images.append(img)
        disch += 1
    else: # Then this is the charge cycle
        plot_voltage_capacity(data=grouped.get_group(index), 
        plot_name='cycles/charge_' + str(ch) + '.png', 
        plot_title=str(ch) + '$^{th}$ charge')

        img = cv2.imread('cycles/charge_' + str(ch) + '.png')
        ch_images.append(img)
        ch += 1


# Save to video in ./cycles/ directory
disch_video = cv2.VideoWriter('cycles/discharge.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 1, size)
ch_video = cv2.VideoWriter('cycles/charge.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 1, size)
for image in disch_images:
    disch_video.write(image)
for image in ch_images:
    ch_video.write(image)
disch_video.release()
ch_video.release()


# Plot all discharge cycles in a single plot
plt.figure()
counter = 0
for index in grouped.indices.keys():
    if grouped.get_group(index)['control/V/mA'].iloc[10] < 0:
        data = grouped.get_group(index)
        plt.plot(-1*data['Q charge/discharge/mA.h'], data['Ewe/V'], color=colorFader(color1, color2, counter/len(disch_images)))
        counter += 1
plt.title('Discharge cycles')
plt.xlabel('Capacity (mAh)')
plt.ylabel('Voltage (V)')
plt.ylim(1.5, 4.8)
plt.savefig('cycles/all_discharge_cycles.png')
plt.show()
plt.close()


# Plot all charge cycles in a single plot
plt.figure()
counter = 0
for index in grouped.indices.keys():
    if grouped.get_group(index)['control/V/mA'].iloc[10] > 0:
        data = grouped.get_group(index)
        plt.plot(data['Q charge/discharge/mA.h'], data['Ewe/V'], color=colorFader(color1, color2, counter/len(ch_images)))
        counter += 1
plt.title('Charge cycles')
plt.xlabel('Capacity (mAh)')
plt.ylabel('Voltage (V)')
plt.ylim(1.5, 4.8)
plt.savefig('cycles/all_charge_cycles.png')
plt.show()
plt.close()
