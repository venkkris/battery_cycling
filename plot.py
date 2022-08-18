"""
Author: Venkatesh Krishnamurthy. Copyright 2022. 
Minor contributions by Chris Eschler.
"""

from galvani import BioLogic
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import cv2
import numpy as np
import glob
import os
from datetime import datetime


###############################################################################
# Important variables
###############################################################################

same_xlim_every_cycle = True     # Uses same xlim i.e. capacity for all cycles
voltage_limits = [1.5, 4.8]      # Voltage limits for all plots
remove_OCV_part = True           # Removes OCV part for plot of each cycle; not removed for time series plots
stitch_files = True              # Stitches together multiple files into one dataframe; use when multiple files are part of one test
dqdv_tol = 0.001                 # Absolute tolerance for dQ/dV


color1 = 'red'
color2 = 'black'
color_ch = '#0069c0'
color_disch = '#0069c0'
color_CE = '#0069c0'
CE_100pc_line = True    # Add line at 100% Coulombic efficiency
# CE_ylim = [1, 101]      # Comment it out to use default ylimits for CE plot

# Note: If plot_all_cycles is false, save_to_video variable is ignored
save_to_video = False   # Save each charge/discharge cycle video or not
plot_all_cycles = False # Save each charge/discharge profile or not
fps = 24                # Frames per second for video

# Other colors
# color = '#0047ab' # Cobalt blue
# color = '#0b1d78' # Dark blue
# color = '#332288' # Dark purple
# color = '#0b1d78' # Dark blue
# color = '#808080' # Gray
# color = '#6b6b6b' # Dark gray

###############################################################################
# Function definitions
###############################################################################

# Helper functions- called by functions but not main
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
    True if discharging, False if charging or no current"""

    # Previous implementation throws errors when number of datapoints is less
    # if group['control/V/mA'].iloc[10] < 0:
    #     return True
    # else:
    #     return False


    # Newer implementation: 
    # Checks for total charge passed in that cycle.
    # If negative, it is discharging
    if group['Q charge/discharge/mA.h'].iloc[-1] < 0:
        return True
    else:
        return False


# Functions: Called by main
def data_tailor():
    """
    Function to stitch data from multiple files into one dataframe.

    In tests with multiple steps, e.g. EIS and GCPL, the Biologic inserts a tag
    into each filename with the type of step. If there are multiple GCPL steps in
    a given test protocol and stitch_files is True, this loop will concatenate them
    into a single dataframe. If either condition is not met, it defaults to the
    first .mpr file it finds.

    Arguments:
    None

    Returns:
    data: A Pandas dataframe instance
    """
    # Read data from mpr file into pandas dataframe object
    gcpl_filelist = glob.glob('*_GCPL_*.mpr')   # List of files with 'GCPL' in filename
    data = pd.DataFrame()   #Initialize empty dataframe

    if len(gcpl_filelist) > 0 and stitch_files:
        for filename in gcpl_filelist:
            mpr_file = BioLogic.MPRfile(filename)
            data = pd.concat([data, pd.DataFrame(mpr_file.data)],ignore_index=True)
    else:
        filename = glob.glob('*.mpr')[0]    # First .mpr file
        mpr_file = BioLogic.MPRfile(filename)
        data = pd.DataFrame(mpr_file.data)
    print(str(datetime.now() - startTime)+' Read data.')
    return data


def plot_time_series(data, quantity, plot_name):
    """
    Plots time series (quantity vs time in hours).

    Arguments: 
    data = pandas dataframe object
    quantity = quantity to be plotted on y axis
    plot_name = plot name

    Returns:
    None
    """
    os.makedirs('time_series',exist_ok=True)
    plt.figure(figsize=(16,4))
    mpl.rcParams['font.size'] = 16
    plt.plot(data['time/s']/3600, data[quantity])
    plt.xlim([0, max(data['time/s'])/3600])
    plt.xlabel('Time (hr)')
    plt.ylabel(quantity)
    plt.savefig(plot_name, bbox_inches='tight')
    plt.close()
    return None


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
    print(str(datetime.now() - startTime)+' Plotted all time series data.')
    return None


def plot_voltage_capacity_ref_initial(data):
    """
    Function to plot voltage vs capacity referenced to initial capacity.
    
    Argument: 
    data = pandas dataframe object

    Returns:
    None
    """

    os.makedirs('main_out',exist_ok=True)
    plt.figure(figsize=(16,4))
    plt.plot(-1*data['(Q-Qo)/mA.h'], data['Ewe/V'], '-')
    plt.xlim([min(-1*data['(Q-Qo)/mA.h']), max(-1*data['(Q-Qo)/mA.h'])])
    plt.xlabel('Capacity (mAh)')
    plt.ylabel('Voltage (V)')
    plt.ylim(voltage_limits)
    plt.savefig('main_out/voltage_vs_capacity.png', bbox_inches='tight')
    plt.close()
    print(str(datetime.now() - startTime)+' Plotted voltage vs capacity ref. initial.')
    return None


def plot_capacity_vs_cycle(data):
    """
    Function to plot charge/discharge capacity vs cycles.
    Also plots Coulombic efficiency vs cycles.

    Argument:
    data = pandas dataframe object
    
    Returns:
    disharge capacity (array), charge capacity (array)
    """

    os.makedirs('main_out',exist_ok=True)
    grouped = data.groupby("half cycle", sort=False)
    disch_capacity = []
    ch_capacity = []

    # Get discharge and charge capacity for each cycle, plot them
    for name, group in grouped:
        if is_it_discharging(group) == True:
            disch_capacity.append(max(-1*group['Q charge/discharge/mA.h']))
        else:
            ch_capacity.append(max(group['Q charge/discharge/mA.h']))

    np.savetxt('main_out/discharge_capacities.txt', np.array(disch_capacity))
    np.savetxt('main_out/charge_capacities.txt', np.array(ch_capacity))

    # Plot Discharge capacity vs cycles
    plt.figure()
    plt.plot(np.arange(start=1, stop=len(disch_capacity)+1, step=1), 
    disch_capacity, linestyle='solid', color=color_disch, linewidth=3, markersize=15)
    plt.xlabel('Number of cycles', 
    fontweight='bold', fontname='Times New Roman', fontsize=20)
    plt.ylabel('Discharge capacity (mAh)', 
    fontweight='bold', fontname='Times New Roman', fontsize=20)
    plt.title('Discharge capacity vs cycles', 
    fontweight='bold', fontname='Times New Roman', fontsize=20)
    plt.xlim(0, len(disch_capacity)+1)
    plt.ylim(0, 1.05*max(disch_capacity))
    plt.minorticks_on()
    plt.tick_params(axis='both', which='minor', length=4, width=1)
    plt.tick_params(axis='both', which='major', labelsize=14, length=7, width=1.5)
    plt.savefig('main_out/discharge_capacity_vs_cycles.png', bbox_inches='tight', dpi=300)
    plt.close()


    # Plot Charge capacity vs cycles
    plt.figure()
    plt.plot(np.arange(start=1, stop=len(ch_capacity)+1, step=1), 
    ch_capacity, linestyle='solid', color=color_ch, linewidth=3, markersize=15)
    plt.xlabel('Number of cycles',
    fontweight='bold', fontname='Times New Roman', fontsize=20)
    plt.ylabel('Charge capacity (mAh)',
    fontweight='bold', fontname='Times New Roman', fontsize=20)
    plt.title('Charge capacity vs cycles',
    fontweight='bold', fontname='Times New Roman', fontsize=20)
    plt.xlim(0, len(ch_capacity)+1)
    plt.ylim(0, 1.05*max(ch_capacity))
    plt.minorticks_on()
    plt.tick_params(axis='both', which='minor', length=4, width=1)
    plt.tick_params(axis='both', which='major', labelsize=14, length=7, width=1.5)
    plt.savefig('main_out/charge_capacity_vs_cycles.png', bbox_inches='tight', dpi=300)
    plt.close()
    print(str(datetime.now() - startTime)+' Plotted charge/discharge capacity vs cycles.')


    # Plot Coulombic efficiency vs cycles
    num_cycles = min(len(ch_capacity), len(disch_capacity))
    x = np.arange(start=1, stop=num_cycles+1, step=1)
    y = np.array(ch_capacity[:num_cycles])/np.array(disch_capacity[:num_cycles])
    y = np.multiply(100, y)

    plt.figure()
    plt.plot(x, y, linestyle='solid', color=color_CE, linewidth=3, markersize=15)

    try:
        plt.ylim(CE_ylim)
    except NameError:
        if CE_100pc_line:       # Plot 100% line
            plt.plot(x, [100]*len(x), 
            linestyle='dashed', color='k', linewidth=3, markersize=15) 
            plt.ylim(min(*y,100)-2, max(*y, 100)+2)
        else:
            plt.ylim(min(y)-2, max(y)+2)
    plt.xlim(1, num_cycles)

    plt.xlabel('Number of cycles',
    fontweight='bold', fontname='Times New Roman', fontsize=20)
    plt.ylabel('Coulombic efficiency (%)',
    fontweight='bold', fontname='Times New Roman', fontsize=20)
    plt.title('Coulombic efficiency vs cycles',
    fontweight='bold', fontname='Times New Roman', fontsize=20)
    plt.minorticks_on()
    plt.tick_params(axis='both', which='minor', length=4, width=1)
    plt.tick_params(axis='both', which='major', labelsize=14, length=7, width=1.5)
    plt.savefig('main_out/coulombic_efficiency_vs_cycles.png', bbox_inches='tight', dpi=300)
    plt.close()
    np.savetxt('main_out/coulombic_efficiencies.txt', np.array(y))
    print(str(datetime.now() - startTime)+' Plotted Coulombic efficiency vs cycles.')

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

    os.makedirs('cycles',exist_ok=True)
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
            if plot_all_cycles:
                plt.figure()
                plt.plot(-1*group['Q charge/discharge/mA.h'], group['Ewe/V'], '-o')
                plt.xlabel('Capacity (mAh)')
                plt.ylabel('Voltage (V)')
                plt.title(str(disch) + '$^{th}$ discharge')
                plt.ylim(voltage_limits)
                if same_xlim_every_cycle == True:
                    plt.xlim([0, max(disch_capacity)])
                plt.savefig('cycles/discharge_' + str(disch) + '.png')
                plt.close()

                if save_to_video:
                    # Add image to array
                    img = cv2.imread('cycles/discharge_' + str(disch) + '.png')
                    height, width, layers = img.shape
                    size = (width, height)
                    disch_images.append(img)

            # Save raw data to csv file
            np.savetxt('cycles/discharge_' + str(disch) + '.csv', 
            np.column_stack((-1*group['Q charge/discharge/mA.h'], group['Ewe/V'])), 
            delimiter=',')
            disch += 1


        # Charge cycle
        else:
            if plot_all_cycles:
                plt.figure()
                plt.plot(group['Q charge/discharge/mA.h'], group['Ewe/V'], '-o')
                plt.xlabel('Capacity (mAh)')
                plt.ylabel('Voltage (V)')
                plt.title(str(ch) + '$^{th}$ charge')
                plt.ylim(voltage_limits)
                if same_xlim_every_cycle == True:
                    plt.xlim([0, max(ch_capacity)])
                plt.savefig('cycles/charge_' + str(ch) + '.png')
                plt.close()

                if save_to_video:
                    # Add image to array
                    img = cv2.imread('cycles/charge_' + str(ch) + '.png')
                    ch_images.append(img)

            # Save raw data to csv file
            np.savetxt('cycles/charge_' + str(ch) + '.csv', 
            np.column_stack((group['Q charge/discharge/mA.h'], group['Ewe/V'])), 
            delimiter=',')
            ch += 1

    if save_to_video:
        # Save videos
        disch_video = cv2.VideoWriter('main_out/discharge_profiles.mp4', 
        cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
        for image in disch_images:
            disch_video.write(image)
        disch_video.release()

        ch_video = cv2.VideoWriter('main_out/charge_profiles.mp4', 
        cv2.VideoWriter_fourcc(*'mp4v'), fps, size)
        for image in ch_images:
            ch_video.write(image)
        ch_video.release()


    ###############################################################################
    # Plot all discharge profiles in a single plot
    ###############################################################################
    plt.figure()
    counter = 0
    for index in grouped.indices.keys():
        if is_it_discharging(grouped.get_group(index)) == True:
            data = grouped.get_group(index)
            plt.plot(-1*data['Q charge/discharge/mA.h'], data['Ewe/V'], 
            color=colorFader(color1, color2, counter/len(disch_capacity)))
            counter += 1
    plt.title('Discharge cycles')
    plt.xlabel('Capacity (mAh)')
    plt.ylabel('Voltage (V)')
    plt.ylim(voltage_limits)
    plt.savefig('main_out/combined_discharge_profiles.png')
    plt.close()


    ###############################################################################
    # Plot all charge profiles in a single plot
    ###############################################################################
    plt.figure()
    counter = 0
    for index in grouped.indices.keys():
        if is_it_discharging(grouped.get_group(index)) == False:
            data = grouped.get_group(index)
            plt.plot(data['Q charge/discharge/mA.h'], data['Ewe/V'], 
            color=colorFader(color1, color2, counter/len(ch_capacity)))
            counter += 1
    plt.title('Charge cycles')
    plt.xlabel('Capacity (mAh)')
    plt.ylabel('Voltage (V)')
    plt.ylim(voltage_limits)
    plt.savefig('main_out/combined_charge_profiles.png')
    plt.close()
    print(str(datetime.now() - startTime)+' Plotted charge/discharge profiles.')


def save_dQ_dV_data(ch_capacity, disch_capacity):
    """
    Function reads from cycles/*_i.csv files and saves to cycles/*_i_dQdV.csv
    where * = 'charge' or 'discharge' and i is integer representing cycle number.
    Uses ch_capacity, disch_capacity to get filenames.
    Columns: voltage, dQ/dV
    """
    filenames = []
    for i in range(len(ch_capacity)):
        filenames.append('cycles/' + 'charge_' + str(i+1) + '.csv')
    for i in range(len(disch_capacity)):
        filenames.append('cycles/' + 'discharge_' + str(i+1) + '.csv')


    for filename in filenames:
        data = pd.read_csv(filename, names=['charge', 'voltage'])

        # Filter data: Remove point if voltage is the same as previous to dqdv_rel_tol V
        q = []
        v = []
        q.append(data['charge'].iloc[0])
        v.append(data['voltage'].iloc[0])
        for i in range(1, len(data)):
            if abs(data['voltage'].iloc[i] - v[-1]) >= dqdv_tol:
                    q.append(data['charge'][i])
                    v.append(data['voltage'][i])
            else:
                continue

        """
        # Compute dQ/dV using centered finite difference;
        # uses forward and backward difference for first and last point
        dqdv = []
        dqdv.append( (q[1]-q[0])/(v[1]-v[0]) )
        for i in range(1, len(q)-1):
            dqdv.append( (q[i+1] - q[i-1])/(v[i+1]-v[i-1]) )
        dqdv.append( (q[-1]-q[-2])/(v[-1]-v[-2]) )
        """
        # Compute dQ/dV using forward difference;
        # uses backward difference for last point
        dqdv = []
        for i in range(len(q)-1):
            dqdv.append( (q[i+1] - q[i])/(v[i+1]-v[i]) )
        dqdv.append( (q[-1]-q[-2])/(v[-1]-v[-2]) )

        # Save to file
        np.savetxt(filename[:-4] + '_dQdV.csv', np.column_stack((v, dqdv)), delimiter=',')
    
    print(str(datetime.now() - startTime)+' Saved dQ/dV data.')
    return None


def save_dV_dQ_data(ch_capacity, disch_capacity):
    """
    Function reads from cycles/*_i.csv files and saves to cycles/*_i_dVdQ.csv
    where * = 'charge' or 'discharge' and i is integer representing cycle number.
    Uses ch_capacity, disch_capacity to get filenames.
    Columns: charge, dQ/dV
    """
    filenames = []
    for i in range(len(ch_capacity)):
        filenames.append('cycles/' + 'charge_' + str(i+1) + '.csv')
    for i in range(len(disch_capacity)):
        filenames.append('cycles/' + 'discharge_' + str(i+1) + '.csv')


    for filename in filenames:
        data = pd.read_csv(filename, names=['charge', 'voltage'])
        # Filter data: Remove point if charge is the same as previous
        q = []
        v = []
        q.append(data['charge'].iloc[0])
        v.append(data['voltage'].iloc[0])
        for i in range(1, len(data)):
            if data['charge'].iloc[i] != q[-1]:
                q.append(data['charge'][i])
                v.append(data['voltage'][i])


        # Compute dV/dQ using centered finite difference; 
        # forward or backward difference for 1st and last point
        dvdq = [ (v[1]-v[0])/(q[1]-q[0]) ]
        for i in range(1, len(q)-1):
            dvdq.append( (v[i+1] - v[i-1])/(q[i+1]-q[i-1]) )
        dvdq.append( (v[-1]-v[-2])/(q[-1]-q[-2]) )

        np.savetxt(filename[:-4] + '_dVdQ.csv', np.column_stack((q, dvdq)), delimiter=',')
    
    print(str(datetime.now() - startTime)+' Saved dV/dQ data.')
    return None


###############################################################################
# Main
###############################################################################
startTime = datetime.now()
print(str(datetime.now() - startTime)+' Started execution.')

# Make directories for plots
os.makedirs('pretty_plots/',exist_ok=True)

data = data_tailor()
plot_all_time_series(data)   
plot_voltage_capacity_ref_initial(data)

# Remove OCV part for all cycles
if remove_OCV_part:
    data.drop(data[data['dQ/mA.h'] == 0].index, inplace=True)

# Plot charge/discharge capacity vs cycles
disch_capacity, ch_capacity = plot_capacity_vs_cycle(data)

# Plot charge/discharge profiles
plot_charge_discharge_profiles(data, disch_capacity, ch_capacity)

# Save dQ/dV, dQ/dV data
save_dQ_dV_data(ch_capacity, disch_capacity)
save_dV_dQ_data(ch_capacity, disch_capacity)


print("%s Finished execution."  % (datetime.now() - startTime) )
###############################################################################

