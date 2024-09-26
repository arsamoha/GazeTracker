import tobii_research as tr
import signal
import sys
import time
from pynput.mouse import Controller
from pynput import keyboard

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

#RM 8/29/24
# This controls the speed of scrolling
Delta = 10
# Replaced this to match the size of my screen
# screen_width, screen_height = 1440, 900
screen_width, screen_height = 1680, 1050

cmba = [{keyboard.Key.shift, keyboard.KeyCode.from_char('a')}, {keyboard.Key.shift, keyboard.KeyCode.from_char('A')}]
cmbz = [{keyboard.Key.shift, keyboard.KeyCode.from_char('z')}, {keyboard.Key.shift, keyboard.KeyCode.from_char('Z')}]
current = set()

deadZoneX = 0.9
deadZoneY = 0.1

# Set the initial pointer location
mouse_position = [screen_width/2, screen_height/2]
mouse.position = tuple(mouse_position)
def gaze_data_callback(gaze_data):
#    center_x = ((gaze_data['left_gaze_point_on_display_area'][0] + gaze_data['right_gaze_point_on_display_area'][0]) / 2) * screen_width
#    center_y = ((gaze_data['left_gaze_point_on_display_area'][1] + gaze_data['right_gaze_point_on_display_area'][1]) / 2) * screen_height

# RM replaced so that center_x and center_y are the gaze coordinates normalized between 0 and 1
    center_x = ((gaze_data['left_gaze_point_on_display_area'][0] + gaze_data['right_gaze_point_on_display_area'][0]) / 2)
    center_y = ((gaze_data['left_gaze_point_on_display_area'][1] + gaze_data['right_gaze_point_on_display_area'][1]) / 2)

# Move the cursor instantly to the gaze point
 #   mouse.position = (center_x, center_y)
 #   print((center_x,center_y))
# RM 8/29/24
    if center_x > deadZoneX:
        mouse_position[0] = screen_width/2 + Delta
    elif center_x < deadZoneY:
        mouse_position[0] = screen_width / 2 - Delta
    else: # dead zone
        mouse_position[0] = screen_width/2
    if center_y > deadZoneX:
        mouse_position[1] = screen_height/2 + Delta
    elif center_y < deadZoneY:
        mouse_position[1] = screen_height/2 - Delta
    else: #dead zone
        mouse_position[1] = screen_height/2

    mouse.position = (mouse_position[0],mouse_position[1])
    #mouse.position = (center_x*screen_width, center_y*screen_height)

    def decrease_zone():
        global deadZoneX
        if 0.5 < deadZoneX <= 0.9:
            deadZoneX -= 0.1
            print('decreasing val')
        else:
            return

    def increase_zone():
        global deadZoneY
        if 0.1 < deadZoneY <= 0.5:
            deadZoneY += 0.1
            print('increasing val')
        else:
            return

    def on_press(key):
        if any([key in z for z in cmba]):
            current.add(key)
            if any(all(k in current for k in z) for z in cmba):
                decrease_zone()
                print(deadZoneX)

        if any([key in z for z in cmbz]):
            current.add(key)
            if any(all(k in current for k in z) for z in cmbz):
                increase_zone()
                print(deadZoneY)

    def on_release(key):
        if any([key in z for z in cmba]):
            current.remove(key)

        # if any([key in z for z in cmbz]):
        #     current.remove(key)

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def signal_handler(sig, frame):
    my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
    sys.exit(0)

# Subscribe to gaze data
my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

signal.signal(signal.SIGINT, signal_handler)

# Keep the program running
while True:
    time.sleep(0.000001)  #Reduce sleep interval to improve responsiveness