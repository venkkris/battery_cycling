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
    if [ -d $dir ]
    then
        if [ $dir != "REBECCA" ]
        then
            echo "\nExecuting in $dir..."
            cp REBECCA/* $dir
            cd $dir
            python plot.py
            cd ..

        else
            continue
        fi
    fi
done
