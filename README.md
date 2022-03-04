## Reduced Effort Biologic Electrochemical Cell Cycling Analysis (REBECCA)
Script(s) to extract battery cycling data from Biologic output file (*.mpr) and make plots for data analysis.

### Installation instructions
Instructions last updated on 4th March 2022.

One of the main dependencies is [Galvani](https://github.com/echemdata/galvani), used to parse the *.mpr file and get a Pandas DataFrame object. It's strongly recommended to create a conda environment for running the script using the provided 'environment.yml' yaml file.

1. Clone the repo using `git clone https://github.com/venkkris/battery_cycling` and switch to that directory/folder.
2. Create a conda environment using the command `conda create --name env_name --file environment.yml`. Replace env_name in the command with your preferred name for the environment. Activate said environment using the `conda activate env_name` command; replace env_name with the name you gave for the conda environment.
3. Preferrably, create a new sub-directory in the battery_cycling/ directory with the plot.py script and the .mpr file in it, and execute the plot.py script using `python plot.py`. 

### Alternate installation instructions
1. Create a conda environment using the command `conda create --name env_name python=3.7`. Replace env_name with a name to your preferrence for the environment.
2. Switch to the newly created conda environment using the command `conda activate env_name`. Replace env_name with the name you gave in the previous step.
3. Next, install required dependencies using the following commands in succession: `pip install numpy`, `pip install scipy`, `pip install matplotlib`, `pip install pandas`, `pip install opencv-python` and `pip install galvani`.
4. Switch to a directory (i.e. folder) of your choice and type the command `git clone https://github.com/venkkris/battery_cycling`. This would create a new directory in your present working directory named battery_cycling and will contain the files needed for the execution of this script.

### Testing
Switch to the test/ directory. Copy plot.py from the parent directory and execute it using the command `python plot.py`. A series of output files will be generated duirng script execution. If you want to clean up the test directory, use the cleanup.sh script from the parent directory.

### Script execution
The script `plot.py` searches for all files with the .mpr extension, reads the electrochemical cycling data from the first such file and plots time series data, capacity vs cycles as well as voltage-capacity profiles for charging as well as discharging.

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
