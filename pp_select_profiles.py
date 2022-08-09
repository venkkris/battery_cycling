import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


###############################################################################
cycle_nums = [5, 10]
filename = 'pretty_plots/select_profiles.png'
voltage_limits = [1.5, 4.8]
color1 = '#53a4ec'
color2 = '#092d4d'
###############################################################################


def colorFader(c1,c2,mix=0):
    """Function to interpolate between two chosen colors.
    fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)"""
    c1=np.array(mpl.colors.to_rgb(c1))
    c2=np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_hex((1-mix)*c1 + mix*c2)


###############################################################################
#               Main
###############################################################################

fig = plt.figure(linewidth=1.5, figsize=(6,5))
ax = fig.add_subplot(111)

ch_cap = []
disch_cap = []
for index, cycle in enumerate(cycle_nums):
    color = colorFader(color1, color2, mix=index/(len(cycle_nums)-1) )
    ch_data = pd.read_csv('cycles/charge_' + str(cycle) + '.csv', 
    names = ['capacity', 'voltage'])
    disch_data = pd.read_csv('cycles/discharge_' + str(cycle) + '.csv',
    names = ['capacity', 'voltage'])
    ch_cap.append(max(ch_data['capacity']))
    disch_cap.append(max(disch_data['capacity']))

    ax.plot(ch_data['capacity'], ch_data['voltage'], label='Cycle ' + str(cycle),
    linestyle='solid', color=color, linewidth=3, markersize=15)
    ax.plot(disch_data['capacity'], disch_data['voltage'],
    linestyle='solid', color=color, linewidth=3, markersize=15)

plt.xlim([0, max(max(ch_cap), max(disch_cap))])
plt.ylim(voltage_limits)

plt.xlabel('Capacity (mAh)', fontsize=20, 
fontname='Times New Roman', fontweight='bold')
plt.ylabel('Voltage (V)', fontsize=20,
fontname='Times New Roman', fontweight='bold')
ax.legend(loc='upper left', fontsize=15)
plt.title('Discharge profiles', fontsize=20,
fontname='Times New Roman', fontweight='bold')

ax.minorticks_on()
ax.tick_params(axis='both', which='minor', length=4, width=1)
ax.tick_params(axis='both', which='major', labelsize=14, length=7, width=1.5)

# Add grid
ax.grid(axis="both", color="black", alpha=.5, linewidth=.5, linestyle=":")

plt.legend(loc='best', fontsize=14)
plt.savefig(filename, dpi=300, bbox_inches='tight')
plt.close()