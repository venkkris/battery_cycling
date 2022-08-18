#!/bin/bash

: '
Author: Venkatesh Krishnamurthy
Copy this script to a folder containing a subfolder named REBECCA with the python scripts inside the subfolder.
All other subfolders must contain the mpr file(s) inside them.
This script will copy all python files inside the REBECCA subfolder into the subfolders and execute them.
'

# Check if REBECCA folder exists
if [ -d "REBECCA" ]; then
    echo "REBECCA folder exists."
else
    echo "REBECCA folder does not exist. Exiting..."
    exit 1
fi

for dir in *
do
    if [ -d $dir ] && [ $dir != "REBECCA" ]      # Check if it's a folder but not named REBECCA
    then
        cd $dir
        # Check if main_out folder exists; skip if it exists in subfolder
        if [ -d "main_out" ]
        then
            echo "\nSkipping $dir because it's been executed before..."
        else
            echo "\nExecuting in $dir..."
            cp ../REBECCA/plot.py .
            python plot.py >> rebecca.log
            rm plot.py                
        fi
        cd ..
    fi
done
