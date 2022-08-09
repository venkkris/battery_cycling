"""
Plots charge, discharge capacity vs cycles.
Also plots CE vs cycles in separate plot.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

color1 = '#1672c0'
color2 = '#c01672'
color_CE = '#72c016'
CE_100pc_line = True

ch_data = pd.read_csv('main_out/charge_capacities.txt', names=['cap'])
disch_data = pd.read_csv('main_out/discharge_capacities.txt', names=['cap'])
ce_data = pd.read_csv('main_out/coulombic_efficiencies.txt', names=['CE'])


# Plot charge, discharge capacity vs cycles
fig = plt.figure(linewidth=1.5, figsize=(6,5))
ax1 = fig.add_subplot(111)

ax1.plot(np.arange(1, len(ch_data)+1) , ch_data['cap'], 
label='Charge', linestyle='solid', 
color=color1, linewidth=3, markersize=15)
ax1.plot(np.arange(1, len(disch_data)+1), disch_data['cap'], 
label='Discharge', linestyle='solid',
color=color2, linewidth=3, markersize=15)

plt.xlim([0, max(len(ch_data), len(disch_data))])
plt.ylim([0, 1.05*max(max(ch_data['cap']), max(disch_data['cap']))])

plt.xlabel('Cycle number',
fontweight='bold', fontname='Times New Roman', fontsize=20)
plt.ylabel('Capacity (mAh)',
fontweight='bold', fontname='Times New Roman', fontsize=20)
plt.title('Capacity vs cycles',
fontweight='bold', fontname='Times New Roman', fontsize=20)
plt.legend(loc='upper right', fontsize=15)

plt.minorticks_on()
plt.tick_params(axis='both', which='minor', length=4, width=1)
plt.tick_params(axis='both', which='major', labelsize=14, length=7, width=1.5)

# Add grid
ax1.grid(axis="both", color="black", alpha=.5, linewidth=.5, linestyle=":")

plt.savefig('pretty_plots/cap_vs_cycles.png', dpi=300, bbox_inches='tight')
plt.close()


# Plot CE vs cycles
fig = plt.figure(linewidth=1.5, figsize=(6,5))
ax1 = fig.add_subplot(111)
ax1.plot(np.arange(1, len(ce_data)+1), ce_data['CE'], 
label='CE', linestyle='solid',
color=color_CE, linewidth=3, markersize=15)
if CE_100pc_line:
    ax1.axhline(y=100, color='k', linestyle='dashed', linewidth=1)

plt.xlim([0, len(ce_data['CE'])])
plt.xlabel('Cycle number',
fontweight='bold', fontname='Times New Roman', fontsize=20)
plt.ylabel('Coulombic efficiency (%)',
fontweight='bold', fontname='Times New Roman', fontsize=20)
plt.title('Coulombic efficiency vs cycles',
fontweight='bold', fontname='Times New Roman', fontsize=20)

plt.minorticks_on()
plt.tick_params(axis='both', which='minor', length=4, width=1)
plt.tick_params(axis='both', which='major', labelsize=14, length=7, width=1.5)

# Add grid
ax1.grid(axis="both", color="black", alpha=.5, linewidth=.5, linestyle=":")

plt.savefig('pretty_plots/CE_vs_cycles.png', dpi=300, bbox_inches='tight')