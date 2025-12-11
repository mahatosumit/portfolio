#!/bin/bash

# Go to rover project directory
cd /home/pi/rover

# Activate virtual environment
source rover_env/bin/activate

# Run your navigation file and save logs
python3 navigation.py >> /home/pi/rover/rover.log 2>&1
