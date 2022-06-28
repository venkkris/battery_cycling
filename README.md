## Reduced Effort Biologic Electrochemical Cell Cycling Analysis (REBECCA)
Script(s) to extract battery cycling data from Biologic output file (*.mpr) and make plots for data analysis.

### Installation instructions
One of the main dependencies is [Galvani](https://github.com/echemdata/galvani), used to parse the *.mpr file and get a Pandas DataFrame object. It's strongly recommended to create a conda environment for running the script using the provided 'environment.yml' yaml file.

1. Clone the repo using `git clone https://github.com/venkkris/battery_cycling` and switch to that directory/folder.
2. Create a conda environment using the command `conda env create --name env_name --file environment.yml`. Replace env_name in the command with your preferred name for the environment. Activate said environment using the `conda activate env_name` command; replace env_name with the name you gave for the conda environment.
3. Preferrably, create a new sub-directory in the battery_cycling/ directory with the plot.py script and the .mpr file in it, and execute the plot.py script using `python plot.py`. 

### Explanation of headers in *.mpr file
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
### Important variables
- 'same_xlim_every_cycle': True/False. If True, uses same x-axis limits for the charge or discharge capacity plots (between zero and max(charge/discharge capacity) being the limits). Set to True if you want to see how the charge or discharge profiles evolve over cycles. Set to false if the discharge or charge capacity in one cycle is over an order of magnitude larger than the discharge or charge capacity in the other cycles.
- 'voltage_limits': Voltage limits for all plots. Default is set to 1.5 V to 4.8 V.
- 'remove_OCV_part': True/False. If True, it removes the equilibriation at the end of a charge or discharge cycle. Makes the combined charge/discharge profile plot prettier, but for deeper analysis such as to know the OCV vs discharge/charge voltage, set to False.
- 'stitch_files': True/False. If True, allows for multiple .mpr files containing "GCPL" to be joined into one Pandas DataFrame. Useful when a given testing protocol generates multiple GCPL .mpr files due to different steps. If False, or if there are no files containing "GCPL" detected, defaults to using the first file found by `glob`.
