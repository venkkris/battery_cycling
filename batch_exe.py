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

path_to_rebecca = '/Users/venkatesh/Desktop/battery_cycling/'

# Test if path_to_rebecca is correct
if not os.path.isdir(path_to_rebecca):
    print('Error: path_to_rebecca is not a directory.')
    exit()
print('Path to REBECCA: ' + path_to_rebecca)
print('\nFiles in REBECCA: ' + str(os.listdir(path_to_rebecca)))
print('\nDoes this look correct? (y/n):')
answer = input()

if answer == 'y':
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
else:
    print('Exiting.')
    exit()
