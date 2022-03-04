"""
Author: Venkatesh Krishnamurthy. Copyright 2022.
"""

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
###############################################################################

same_xlim_every_cycle = False     # Uses same xlim i.e. charge/discharge capacity for all cycles
voltage_limits = [1.5, 4.8]      # Voltage limits for all plots
remove_OCV_part = True           # Removes OCV part for plot of each cycle; not removed for time series plots
color1 = 'red'
color2 = 'black'

###############################################################################
# Function definitions
###############################################################################

def colorFader(c1,c2,mix=0):
    """Function to interpolate between two chosen colors.
    fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)"""
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)


def is_it_discharging(group):
    """Function to check if the battery is discharging.

    Argument:
    group = pandas dataframe group

    Returns:
    True if discharging, False if charging"""
    if group['control/V/mA'].iloc[10] < 0:
        return True
    else:
        return False


def plot_time_series(data, quantity, plot_name):
    """Plots time series (quantity vs time in hours).

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


def plot_all_time_series(data):
    """Function to plot all the time series plots.
    Plots:
    Voltage vs time
    Charge/discharge capacity per cycle vs time
    Charge/discharge capacity ref. to initial capacity vs time
    Control voltage/current vs time
    dQ (difference in charge between time steps i.e. current * dt) vs time
    Ns (input conditions i.e. 1, 2 or 3) vs time
    Half cycle number vs time


    Arguments:
    data = pandas dataframe object"""
    plot_time_series(data=data, quantity='Ewe/V', plot_name='time_series/voltage.png')
    plot_time_series(data=data, quantity='Q charge/discharge/mA.h', plot_name='time_series/charge_per_cycle.png')
    plot_time_series(data=data, quantity='(Q-Qo)/mA.h', plot_name='time_series/charge_referenced_to_initial.png')
    plot_time_series(data=data, quantity='control/V/mA', plot_name='time_series/control.png')
    plot_time_series(data=data, quantity='dQ/mA.h', plot_name='time_series/dQ.png')
    plot_time_series(data=data, quantity='Ns', plot_name='time_series/Ns.png')
    plot_time_series(data=data, quantity='half cycle', plot_name='time_series/half_cycle.png')


def plot_voltage_capacity_ref_initial(data):
    """Function to plot voltage vs capacity referenced to initial capacity.
    
    Argument: 
    data = pandas dataframe object"""
    plt.figure()
    plt.plot(-1*data['(Q-Qo)/mA.h'], data['Ewe/V'], '-')
    plt.xlabel('Capacity (mAh)')
    plt.ylabel('Voltage (V)')
    plt.ylim(voltage_limits)
    plt.savefig('voltage_vs_capacity.png')
    plt.close()


def plot_capacity_vs_cycle(data):
    """Function to plot charge/discharge capacity vs cycles.

    Argument:
    data = pandas dataframe object
    
    Returns:
    disharge capacity (array), charge capacity (array)
    """

    grouped = data.groupby("half cycle", sort=False)
    disch_capacity = []
    ch_capacity = []

    # Get discharge and charge capacity for each cycle, plot them
    for name, group in grouped:
        if is_it_discharging(group) == True:
            disch_capacity.append(max(-1*group['Q charge/discharge/mA.h']))
        else:
            ch_capacity.append(max(group['Q charge/discharge/mA.h']))

    np.savetxt('discharge_capacities.txt', np.array(disch_capacity))
    np.savetxt('charge_capacities.txt', np.array(ch_capacity))

    plt.figure()
    plt.plot(np.arange(start=1, stop=len(disch_capacity)+1, step=1), 
    disch_capacity, '-o')
    plt.xlabel('Number of cycles')
    plt.ylabel('Discharge capacity (mAh)')
    plt.xlim(1, len(disch_capacity)+1)
    plt.ylim(0, 1.05*max(disch_capacity))
    plt.title('Discharge capacity vs Number of cycles')
    plt.savefig('discharge_capacity_vs_cycles.png')
    plt.close()

    plt.figure()
    plt.plot(np.arange(start=1, stop=len(ch_capacity)+1, step=1), 
    ch_capacity, '-o')
    plt.xlabel('Number of cycles')
    plt.ylabel('Charge capacity (mAh)')
    plt.xlim(1, len(ch_capacity)+1)
    plt.ylim(0, 1.05*max(ch_capacity))
    plt.title('Charge capacity vs Number of cycles')
    plt.savefig('charge_capacity_vs_cycles.png')
    plt.close()
    return disch_capacity, ch_capacity


def plot_charge_discharge_profiles(data, disch_capacity, ch_capacity):
    """Plots charge/discharge profiles for each cycle in cycles/ directory,
    makes a video of those plots, and
    plots all charge and discharge profiles in a single plot.

    Arguments:
    data = Pandas DataFrame object
    disch_capacity = array of discharge capacities 
    ch_capacity + array of charge capacities
    
    Note:
    arrays of ch. and disch. capacities are returned by plot_capacity_vs_cycle
    """
    disch_images = []   # Array of discharge images
    ch_images = []      # Array of charge images
    disch = 1
    ch = 1


    ###############################################################################
    # Plot each charge and discharge profile in cycles/ directory
    ###############################################################################
    grouped = data.groupby("half cycle", sort=False)
    for name, group in grouped:

        # If discharge i.e. current is negative
        if is_it_discharging(group) == True:
            plt.figure()
            plt.plot(-1*group['Q charge/discharge/mA.h'], group['Ewe/V'], '-o')
            plt.xlabel('Capacity (mAh)')
            plt.ylabel('Voltage (V)')
            plt.title(str(disch) + '$^{th}$ discharge')
            plt.ylim(voltage_limits)
            if same_xlim_every_cycle == True:
                plt.xlim = ([0, max(disch_capacity)])
            plt.savefig('cycles/discharge_' + str(disch) + '.png')
            plt.close()

            img = cv2.imread('cycles/discharge_' + str(disch) + '.png')
            height, width, layers = img.shape
            size = (width, height)
            disch_images.append(img)
            disch += 1

        # Charge cycle
        else:
            plt.figure()
            plt.plot(group['Q charge/discharge/mA.h'], group['Ewe/V'], '-o')
            plt.xlabel('Capacity (mAh)')
            plt.ylabel('Voltage (V)')
            plt.title(str(ch) + '$^{th}$ charge')
            plt.ylim(voltage_limits)
            if same_xlim_every_cycle == True:
                plt.xlim = ([0, max(ch_capacity)])
            plt.savefig('cycles/charge_' + str(ch) + '.png')
            plt.close()

            img = cv2.imread('cycles/charge_' + str(ch) + '.png')
            ch_images.append(img)
            ch += 1


    # Save to video
    disch_video = cv2.VideoWriter('discharge_profiles.mp4', 
    cv2.VideoWriter_fourcc(*'mp4v'), 1, size)
    ch_video = cv2.VideoWriter('charge_profiles.mp4', 
    cv2.VideoWriter_fourcc(*'mp4v'), 1, size)
    for image in disch_images:
        disch_video.write(image)
    for image in ch_images:
        ch_video.write(image)
    disch_video.release()
    ch_video.release()


    ###############################################################################
    # Plot all discharge profiles in a single plot
    ###############################################################################
    plt.figure()
    counter = 0
    for index in grouped.indices.keys():
        if grouped.get_group(index)['control/V/mA'].iloc[10] < 0:
            data = grouped.get_group(index)
            plt.plot(-1*data['Q charge/discharge/mA.h'], data['Ewe/V'], 
            color=colorFader(color1, color2, counter/len(disch_images)))
            counter += 1
    plt.title('Discharge cycles')
    plt.xlabel('Capacity (mAh)')
    plt.ylabel('Voltage (V)')
    plt.ylim(1.5, 4.8)
    plt.savefig('combined_discharge_profiles.png')
    plt.close()


    ###############################################################################
    # Plot all charge profiles in a single plot
    ###############################################################################
    plt.figure()
    counter = 0
    for index in grouped.indices.keys():
        if grouped.get_group(index)['control/V/mA'].iloc[10] > 0:
            data = grouped.get_group(index)
            plt.plot(data['Q charge/discharge/mA.h'], data['Ewe/V'], 
            color=colorFader(color1, color2, counter/len(ch_images)))
            counter += 1
    plt.title('Charge cycles')
    plt.xlabel('Capacity (mAh)')
    plt.ylabel('Voltage (V)')
    plt.ylim(1.5, 4.8)
    plt.savefig('combined_charge_profiles.png')
    plt.close()


###############################################################################
# Main
###############################################################################

# Make directories for plots
os.makedirs('time_series', exist_ok=True)
os.makedirs('cycles', exist_ok=True)

# Read data from mpr file into pandas dataframe object
filename = glob.glob('*.mpr')[0]
mpr_file = BioLogic.MPRfile(filename)
data = pd.DataFrame(mpr_file.data)

# Plot all imp. time series data
plot_all_time_series(data)

# Plot voltage vs capacity referenced to initial capacity
plot_voltage_capacity_ref_initial(data)

# Remove OCV part for all cycles
if remove_OCV_part:
    data.drop(data[data['dQ/mA.h'] == 0].index, inplace=True)

# Plot charge/discharge capacity vs cycles
disch_capacity, ch_capacity = plot_capacity_vs_cycle(data)

# Plot charge/discharge profiles
plot_charge_discharge_profiles(data, disch_capacity, ch_capacity)
###############################################################################

###############################################################################
