#!/bin/bash
# Author: Venkatesh Krishnamurthy
# This script is used to clear all previous plots, videos and txt files and then execute plot.py
clear
rm cycles/*
rm time_series/*
rm *.png
rm *.txt
rm *.mp4
/Users/venkatesh/.anaconda3/envs/galvani/bin/python plot.py
# ls
