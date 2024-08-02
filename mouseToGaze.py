import tobii_research as tr
import signal
import sys
import time
from pynput.mouse import Controller

# Find all connected eye trackers
found_eyetrackers = tr.find_all_eyetrackers()

my_eyetracker = found_eyetrackers[0]
print("Address: " + my_eyetracker.address)
print("Model: " + my_eyetracker.model)
print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
print("Serial number: " + my_eyetracker.serial_number)

if not found_eyetrackers:
    print("No eye trackers found")
    sys.exit()

mouse = Controller()

def gaze_data_callback(gaze_data):
    screen_width, screen_height = 1680, 1050
    center_x = ((gaze_data['left_gaze_point_on_display_area'][0] + gaze_data['right_gaze_point_on_display_area'][0]) / 2) * screen_width
    center_y = ((gaze_data['left_gaze_point_on_display_area'][1] + gaze_data['right_gaze_point_on_display_area'][1]) / 2) * screen_height

    # Move the cursor instantly to the gaze point
    mouse.position = (center_x, center_y)

def signal_handler(sig, frame):
    my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
    sys.exit(0)

# Subscribe to gaze data
my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

signal.signal(signal.SIGINT, signal_handler)

# Keep the program running
while True:
    time.sleep(1)  #Reduce sleep interval to improve responsiveness