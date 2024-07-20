import tobii_research as tr
import time
from tkinter import *

root = Tk()
root.geometry("330x220+300+300")

canvas = Canvas(root)
canvas.pack(fill=BOTH, expand=1)

found_eyetrackers = tr.find_all_eyetrackers()

if not found_eyetrackers:
    print("No eye trackers found")
    exit()

my_eyetracker = found_eyetrackers[0]
print("Address: " + my_eyetracker.address)
print("Model: " + my_eyetracker.model)
print("Name (It's OK if this is empty): " + my_eyetracker.device_name)
print("Serial number: " + my_eyetracker.serial_number)

def gaze_data_callback(gaze_data):
    # Clear the canvas
    canvas.delete("all")

    # Get the canvas width and height
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Convert gaze data to canvas coordinates
    left_x = gaze_data['left_gaze_point_on_display_area'][0] * canvas_width
    left_y = gaze_data['left_gaze_point_on_display_area'][1] * canvas_height
    right_x = gaze_data['right_gaze_point_on_display_area'][0] * canvas_width
    right_y = gaze_data['right_gaze_point_on_display_area'][1] * canvas_height

    # Draw an oval at the gaze point
    # canvas.create_oval(left_x - 5, left_y - 5, left_x + 5, left_y + 5, outline="#f11", fill="#1f1", width=2)
    # canvas.create_oval(right_x - 5, right_y - 5, right_x + 5, right_y + 5, outline="#f11", fill="#1f1", width=2)

    canvas.create_oval(((left_x - 5) + (right_x - 5))/2, (((left_y - 5) + (right_y - 5))/2), (((left_x + 5) + (right_x + 5))/2), (((left_y + 5) + (right_y + 5))/2))

    print("Left eye: ({left_x}, {left_y}) \t Right eye: ({right_x}, {right_y})".format(
        left_x=left_x, left_y=left_y,
        right_x=right_x, right_y=right_y))

my_eyetracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

root.mainloop()

time.sleep(5)

my_eyetracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback)
