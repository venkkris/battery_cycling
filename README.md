# battery_cycling
Script(s) to extract battery cycling data from Biologic output file (*.mpr) and make plots

# Installation instructions


## Explanation of headers in *.mpr file
```
'flags': Flags
'Ns': Input conditions
'time/s': Time in seconds
'dQ/mA.h': Change transferred in time step; essentially current
'(Q-Qo)/mA.h': Capacity referenced to initial capacity
'control/V/mA': Control voltage or current
'Ewe/V': Voltage of the cell
'Q charge/discharge/mA.h': Capacity discharged or charged; resets to zero after switching cycles; negative for discharge
'half cycle': No idea; probably an index of when it switches from charging to discharging
```