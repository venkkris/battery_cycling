"""
Instructions for use:
1. Copy all mpr files and this script into a folder.
2. Specify path to the REBECCA root folder.
3. This script creates a folder named after each mpr file,
    copies all python scripts from REBECCA root folder,
    and runs the plot.py script in each subfolder.
"""

import os
import glob

path_to_rebecca = '~/Desktop/battery_cycling/'

mpr_files = glob.glob('*.mpr')
for mpr_file in mpr_files:
    print('Processing {}.'.format(mpr_file))
    os.system('mkdir ' + mpr_file[:-4])
    os.system('mv ' + mpr_file + ' ' + mpr_file[:-4])
    os.system('cp ' + path_to_rebecca + '*.py ' + mpr_file[:-4])
    os.chdir(mpr_file[:-4])
    os.system('python plot.py')
    os.chdir('..')
    print('Done.')
