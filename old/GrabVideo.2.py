# pip install opencv-python
# pip install keyboard
# pip install pillow
import cv2
import ctypes
import keyboard
import threading
import PIL.Image, PIL.ImageTk

from time import time as now
from tkinter import *

last_ctrl_press = None
last_ctrl_press_count = 0
window_visible = False
video_capture = None

def keyboard_hook(event):
    global last_ctrl_press
    global last_ctrl_press_count
    if event.event_type == 'up':
        match event.name:
            case 'ctrl':
                if last_ctrl_press_count == 0:
                    last_ctrl_press = now()
                    last_ctrl_press_count = 1
                elif now() - last_ctrl_press < 500:
                    last_ctrl_press_count = last_ctrl_press_count + 1
                    if last_ctrl_press_count >= 3:
                        toggle_window()
                        last_ctrl_press = None
                        last_ctrl_press_count = 0
                else:
                    last_ctrl_press = now()
                    last_ctrl_press_count = 1
            case 'esc':
                close()
            case _:
                last_ctrl_press = None
                last_ctrl_press_count = 0

def show():
    global root
    global window_visible
    window_visible = True
    update_image()
    root.deiconify()
 
def hide():
    global root
    global window_visible
    window_visible = False
    root.withdraw()
    
def close():
    global root
    hide()
    root.destroy()

def toggle_window():
    global window_visible
    if window_visible:
        hide()
    else:
        show()

def open_camera():
    global canvas
    global root
    global video_capture
    # initialize video capture object to read video from external webcam
    video_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW) # CAP_ANY?
    if not video_capture.isOpened():
        print("Could not open any camera")
        exit(1)

    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)
    
    # this call somehow initializes the camera
    ret, frame = video_capture.read()

def update_image():   
    global canvas
    global root
    global video_capture
    global panel
    if video_capture.isOpened():
        # read video frame by frame
        ret, frame = video_capture.read()

        if ret:
            frame_height, frame_width, _ = frame.shape

            scaleWidth = float(screen_width)/float(frame_width)
            scaleHeight = float(screen_height)/float(frame_height)
            
            frame = cv2.resize(frame,None,fx=scaleWidth,fy=scaleHeight,interpolation=cv2.INTER_CUBIC)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = PIL.Image.fromarray(image)
            image = PIL.ImageTk.PhotoImage(image)
        
            panel.configure(image=image)
            panel.image = image 
            
    if window_visible:
        root.after(10, update_image)

def close_camera():
    video_capture.release()
    
user32 = ctypes.windll.user32
screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

root = Tk()
root.title("SoftKVM")
root.wm_attributes('-topmost', 'true')
root.wm_attributes('-fullscreen','true')
hide()

panel = Label(root, highlightthickness=0)
panel.image = None
panel.pack(padx=0, pady=0)

open_camera()

keyboard.hook(keyboard_hook, False)

print("SoftKVM started")

root.mainloop()

close_camera()

keyboard.unhook_all()

