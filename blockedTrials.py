#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import csv
import tobii_research as tr

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))

# Store info about the experiment session
expName = 'blockedTrials'
expInfo = {'session': '001', 'participant': ''}
expInfo['date'] = time.strftime("%Y-%m-%d_%H-%M-%S")
expInfo['expName'] = expName

# Data file name stem = absolute path + name
filename = os.path.join(_thisDir, 'data', '{}_{}_{}'.format(expInfo['participant'], expName, expInfo['date']))

# Find eye trackers
found_eyetrackers = tr.find_all_eyetrackers()
# Select the first eye tracker
if found_eyetrackers:
    my_eyetracker = found_eyetrackers[0]
else:
    print("No eye tracker found!")
    sys.exit()

# Create list to store gaze data
gaze_list = []

# Create callback to get gaze data
def gaze_data_callback(gaze_data):
    gaze_list.append([gaze_data['system_time_stamp'], gaze_data['device_time_stamp'],
                      gaze_data['left_gaze_point_on_display_area'],
                      gaze_data['right_gaze_point_on_display_area']])

# Start getting gaze data
my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

# Experiment loop
try:
    while True:
        time.sleep(1)  # Run the experiment as long as needed
except KeyboardInterrupt:
    pass  # Terminate the experiment when the user interrupts it

# Stop getting gaze data
my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)

# Save gaze data to a CSV file
if gaze_list:
    with open(filename + '_et.csv', 'w') as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(['ts', 'etts', 'gpl', 'gpr'])  # Header
        for row in gaze_list:
            w.writerow(row)  # Write row in CSV
else:
    print("No gaze data to save!")
