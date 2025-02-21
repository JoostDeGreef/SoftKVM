# pip install opencv-python
# pip install keyboard
import cv2
import ctypes
import keyboard
import threading

from time import time as now
from enum import Enum

class Command(Enum):
    NOP = 0
    DISPLAY_TOGGLE = 1
    DISPLAY_ON = 2
    DISPLAY_OFF = 3
    EXIT = 4

command_event = threading.Event()
command = Command.NOP
last_ctrl_press = None
last_ctrl_press_count = 0

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
                        command = Command.DISPLAY_TOGGLE
                        command_event.set()
                        last_ctrl_press = None
                        last_ctrl_press_count = 0
                else:
                    last_ctrl_press = now()
                    last_ctrl_press_count = 1
            case 'esc':
                command = Command.EXIT
                command_event.set()
            case _:
                last_ctrl_press = None
                last_ctrl_press_count = 0

def display():
    window_name = 'SoftKVM'
    # get Screen Size
    user32 = ctypes.windll.user32
    screen_width, screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

    # initialize video capture object to read video from external webcam
    video_capture = cv2.VideoCapture(0,cv2.CAP_DSHOW) # CAP_ANY?
    if not video_capture.isOpened():
        print("Could not open any camera")
        exit(1)

    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)

    # Full screen mode
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_VISIBLE, 0)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
    
    while (video_capture.isOpened() and not command_event.is_set()): 
        # read video frame by frame
        ret, frame = video_capture.read()

        if ret:
            frame_height, frame_width, _ = frame.shape

            # print("{}x{}".format(frame_width,frame_height))

            scaleWidth = float(screen_width)/float(frame_width)
            scaleHeight = float(screen_height)/float(frame_height)
      
            frame = cv2.resize(frame,None,fx=scaleWidth,fy=scaleHeight,interpolation=cv2.INTER_CUBIC)
            cv2.imshow(window_name, frame)
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    # release video capture object
    video_capture.release()
    cv2.destroyAllWindows()

keyboard.hook(keyboard_hook, False)
display()
keyboard.unhook_all()
