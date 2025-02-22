# pip install opencv-python
# pip install keyboard
# pip install pillow

import Setup # Has to be first!
import keyboard
import threading
import argparse
import sys
import ipaddress

from Display_OpenCV import Display_OpenCV as display_opencv
from Display_pyGame import Display_pyGame as display_pygame
from Window_TK import Window_TK as window_tk
from Window_pyGame import Window_pyGame as window_pygame

from time import time as now
   
class SoftKVMApp:
    def __init__(self, window):
        # variables for keyboard_hook
        self.last_ctrl_press = None
        self.last_ctrl_press_count = 0
        self.window = window
        # hooking keyboard
        print("[SoftKVM] setting keyboard hook")
        keyboard.hook(self.keyboard_hook, False)

    def run(self):
        print("[SoftKVM] Started!")
        self.window.run()

    def close(self):
        print("[SoftKVM] Closing down")
        self.window.hide()
        keyboard.unhook_all()
        self.window.destroy()
       
    def keyboard_hook(self, event):
        if event.event_type == 'up':
            match event.name:
                case 'ctrl':
                    if self.last_ctrl_press_count == 0:
                        self.last_ctrl_press = now()
                        self.last_ctrl_press_count = 1
                    elif now() - self.last_ctrl_press < 500:
                        self.last_ctrl_press_count = self.last_ctrl_press_count + 1
                        if self.last_ctrl_press_count >= 3:
                            self.window.toggle()
                            self.last_ctrl_press = None
                            self.last_ctrl_press_count = 0
                    else:
                        self.last_ctrl_press = now()
                        self.last_ctrl_press_count = 1
                case 'esc':
                    self.close()
                case _:
                    self.last_ctrl_press = None
                    self.last_ctrl_press_count = 0
        else:
            pass

class MatchChoices(object):
    def __init__(self, choices):
        self.choices = choices
    def __call__(self, choice):
        for c in self.choices:
            if c.casefold() == choice.casefold():
                return c
        raise argparse.ArgumentTypeError(f"{choice} does not follow the expected pattern ({choices}).")

class MatchIP(object):
    def __call__(self, address):
        try:
            return ipaddress.ip_address(address)
        except ValueError:
            raise argparse.ArgumentTypeError(f"{address} is not a valid IP address.")
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='SoftKVM',
        description='A program which mimmicks a KVM in software, by grabbing video using hdmi2usb, and emulating a usb keyboard and mouse using a pi zero2W.',
        epilog='(C) 2025, Joost de Greef <Joost@stack.nl>')
    choices=['TK', 'pyGame']
    parser.add_argument("-d", "--display", choices=choices, type=MatchChoices(choices), default="TK", help="Choose a display framework")
    choices=['OpenCV', 'pyGame']
    parser.add_argument("-c", "--camera", choices=choices, type=MatchChoices(choices), default="OpenCV", help="Choose a camera (hdmi2usb) framework")
    parser.add_argument("-a", "--address", type=MatchIP(), default="127.0.0.1", help="IP address for the SoftKMV-pi")
    args = parser.parse_args()
    display = None
    match args.camera:
        case 'OpenCV':
            display = display_opencv()
        case 'pyGame':
            display = display_pygame()
        case _:
            print("Unsupported 'camera' argument. This is probably a bug")
            parser.print_help()
            sys.exit(1)
    window = None
    match args.display:
        case 'TK':
            window = window_tk(display)
        case 'PYGAME':
            window = window_tk(display)
        case _:
            print("Unsupported 'display' argument. This is probably a bug")
            parser.print_help()
            sys.exit(1)
    # start main loop
    SoftKVMApp(window).run()
    print("[SoftKVM] All done")
