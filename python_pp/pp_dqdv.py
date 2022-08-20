import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

def colorFader(c1,c2,mix=0):
    """Function to interpolate between two chosen colors.
    fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)"""
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)


def smoothen_dqdv(data, smooth_type):
    """
    Smoothen the dQ/dV data.
    Currently implements rolling average of 3 and Savitzky-Golay.

    Arguments:
    data -- dataframe with V, dQ/dV as columns
    smooth_type -- string, either 'savitzky-golay' or 'rolling'

    Returns:
    data -- dataframe with V and smoothed dQ/dV as columns.
    """

    if smooth_type == 'rolling':
        data['dqdv'] = data['dqdv'].rolling(3).mean()

    elif smooth_type == 'savitzky_golay':
        raise NotImplementedError

    return data


###############################################################################
cycle_nums = [5, 10]
voltage_limits = [1.5, 4.8]         # x limits
smooth_type = 'rolling'           # 'None', 'rolling' or 'savitzky-golay'

dqdv_color1 = '#53a4ec'
dqdv_color2 = '#092d4d'
###############################################################################


for index, cycle_num in enumerate(cycle_nums):
    color = colorFader(dqdv_color1, dqdv_color2, mix=index/len(cycle_nums))
    # Charge data
    ch_data = pd.read_csv('cycles/charge_'+str(cycle_num)+'_dQdV.csv', 
    names=['voltage', 'dqdv'])
    ch_data = smoothen_dqdv(ch_data, smooth_type)
    plt.plot(ch_data['voltage'], ch_data['dqdv'], label='Cycle '+str(cycle_num),
    linestyle='solid', color=color, linewidth=3, markersize=15)

    # Horizontal line at 0
    plt.axhline(y=0, color='black', linestyle='dashed', linewidth=1.5)

    # Discharge data
    disch_data = pd.read_csv('cycles/discharge_'+str(cycle_num)+'_dQdV.csv', 
    names=['voltage', 'dqdv'])
    disch_data = smoothen_dqdv(disch_data, smooth_type)
    plt.plot(disch_data['voltage'], disch_data['dqdv'],
    linestyle='solid', color=color, linewidth=3, markersize=15)


plt.xlabel('Voltage (V)',
fontweight='bold', fontname='Times New Roman', fontsize=20)
plt.ylabel('dq/dV (mAh/V)',
fontweight='bold', fontname='Times New Roman', fontsize=20)
plt.title('Differential capacity',
fontweight='bold', fontname='Times New Roman', fontsize=20)
plt.legend(loc='best', fontsize=15)

plt.xlim(voltage_limits)
plt.minorticks_on()
plt.tick_params(axis='both', which='minor', length=4, width=1)
plt.tick_params(axis='both', which='major', labelsize=14, length=7, width=1.5)

plt.savefig('pretty_plots/dQdV.png', dpi=300, bbox_inches='tight')
plt.close()
