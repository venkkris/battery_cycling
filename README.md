# Reduced Effort Biologic Electrochemical Cell Cycling Analysis (REBECCA)
Script(s) to extract battery cycling data from Biologic output file (*.mpr) and make plots for data analysis.

# Installation instructions
One of the main dependencies is [Galvani](https://github.com/echemdata/galvani), used to parse the *.mpr file and get a Pandas DataFrame object. It's strongly recommended to create a conda environment for running the script using the provided 'environment.yml' yaml file.

1. Clone the repo using `git clone https://github.com/venkkris/battery_cycling` and switch to that directory/folder.
2. Create a conda environment using the command `conda env create --name env_name --file environment.yml`. Replace env_name in the command with your preferred name for the environment. Activate said environment using the `conda activate env_name` command; replace env_name with the name you gave for the conda environment.
3. Preferrably, create a new sub-directory in the battery_cycling/ directory with the plot.py script and the .mpr file in it, and execute the plot.py script using `python plot.py`. 

# Explanation of headers in *.mpr file
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
