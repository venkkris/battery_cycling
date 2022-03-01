#!/bin/bash
clear
rm discharge.mp4
rm charge.mp4
rm cycles/*

/Users/venkatesh/.anaconda3/envs/galvani/bin/python plot.py
ls
# open discharge.mp4
