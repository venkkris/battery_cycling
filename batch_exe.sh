#!/bin/bash

# Absolute path to REBECCA
REBECCA_PATH="/Users/venkatesh/Desktop/battery_cycling/"

# List files in REBECCA_PATH, ask user if files are correct
echo "Listing files in REBECCA folder:"
ls $REBECCA_PATH
echo "Is this the correct path to REBECCA? (y/n)"
read answer

if [ $answer = "y" ]; then
    echo "Starting batch processing..."

    for file in *.mpr
    do
        echo
        echo "Processing $file"
        mkdir "${file%.*}"
        mv $file ${file%.*}
        cd ${file%.*}
        cp $REBECCA_PATH*.py .
        python plot.py
        cd ..
    done

else
    echo "Exiting"
fi

unset REBECCA_PATH