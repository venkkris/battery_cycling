
from galvani import BioLogic
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import cv2
import numpy as np
import glob
import os

###############################################################################
# Important variables
voltage_limits = [1.5, 4.8]     # Voltage limits for all plots
remove_OCV_part = True          # Removes OCV part for plot of each cycle; not removed for time series plots
same_xlim_every_cycle = True    # Uses same xlim i.e. charge/discharge capacity for all cycles
###############################################################################
# Function definitions


def colorFader(c1,c2,mix=0):
    """Function to interpolate between two chosen colors.
    fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)"""
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)


def plot_time_series(data, quantity, plot_name):
    """Function to plot time series of voltage vs time.

    Arguments: 
    data = pandas dataframe object
    quantity = quantity to be plotted on y axis
    plot_name = plot name"""
    plt.figure()
    plt.plot(data['time/s']/3600, data[quantity])
    plt.xlabel('Time (hr)')
    plt.ylabel(quantity)
    plt.savefig(plot_name)
    plt.close()


def plot_voltage_capacity(data, plot_name, plot_title):
    """ Function to plot voltage vs capacity.

    Arguments:
    data = pandas dataframe object
    plot_name = plot name
    plot_title = plot title"""
    plt.figure()
#    plt.plot(-1*data['(Q-Qo)/mA.h'], data['Ewe/V'], '-*')
    plt.plot(-1*data['Q charge/discharge/mA.h'], data['Ewe/V'], '-o')
    plt.xlabel('Capacity (mAh)')
    plt.ylabel('Voltage (V)')
    plt.title(plot_title)
    plt.ylim(voltage_limits)
    plt.savefig(plot_name)
    plt.close()


def plot_all_time_series(data):
    """Function to plot all the time series plots.

    Arguments:
    data = pandas dataframe object"""
    plot_time_series(data=data, quantity='Ewe/V', plot_name='time_series/voltage.png')
    plot_time_series(data=data, quantity='Q charge/discharge/mA.h', plot_name='time_series/charge_per_cycle.png')
    plot_time_series(data=data, quantity='(Q-Qo)/mA.h', plot_name='time_series/charge_referenced_to_initial.png')
    plot_time_series(data=data, quantity='control/V/mA', plot_name='time_series/control.png')
    plot_time_series(data=data, quantity='dQ/mA.h', plot_name='time_series/dQ.png')
    plot_time_series(data=data, quantity='Ns', plot_name='time_series/Ns.png')
    plot_time_series(data=data, quantity='half cycle', plot_name='time_series/half_cycle.png')

  
###############################################################################
# Main
# Make directories for plots
os.makedirs('time_series',exist_ok=True)
os.makedirs('cycles',exist_ok=True)

# Read data from mpr file into pandas dataframe object
filename = glob.glob('*.mpr')[0]
mpr_file = BioLogic.MPRfile(filename)
data = pd.DataFrame(mpr_file.data)

# Plot all imp. time series data
plot_all_time_series(data)

# Plot voltage vs capacity referenced to initial capacity
plt.figure()
plt.plot(-1*data['(Q-Qo)/mA.h'], data['Ewe/V'], '-')
plt.xlabel('Capacity (mAh)')
plt.ylabel('Voltage (V)')
plt.ylim(voltage_limits)
plt.title('Voltage vs Capacity')
plt.savefig('voltage_vs_capacity.png')
plt.close()


###############################################################################
# Plot cycling data
# Assumption: Always start with 1st discharge, then 1st charge
disch = 1           # Index
ch = 1              # Index
disch_images = []   # Array of discharge images
ch_images = []      # Array of charge images
color1 = 'red'
color2 = 'black'

# Remove OCV part for all cycles
if remove_OCV_part:
    data.drop(data[data['dQ/mA.h'] == 0].index, inplace=True)

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


# Save to video
disch_video = cv2.VideoWriter('discharge.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 1, size)
ch_video = cv2.VideoWriter('charge.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 1, size)
for image in disch_images:
    disch_video.write(image)
for image in ch_images:
    ch_video.write(image)
disch_video.release()
ch_video.release()


###############################################################################
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
plt.savefig('all_discharge_cycles.png')
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
plt.savefig('all_charge_cycles.png')
plt.close()
###############################################################################