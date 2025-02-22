import Setup # Has to be the first! This will update environment settings other modules use.

import keyboard
import threading
import argparse
import sys
import ipaddress
import webbrowser

from Display_OpenCV import Display_OpenCV as display_opencv
from Display_pyGame import Display_pyGame as display_pygame
from Window_TK import Window_TK as window_tk
from Window_pyGame import Window_pyGame as window_pygame
import Menu

from time import time as now
   
class SoftKVMApp:
    def __init__(self, window, display):
        # variables for keyboard_hook
        self.last_ctrl_press = None
        self.last_ctrl_press_count = 0
        self.window = window(display)
        self.menu = Menu.Menu(on_exit=self.close, on_about=self.about, on_switch=self.switch)

    def __del__(self):
        self.menu = None
        self.window = None
        
    def run(self):
        print("[SoftKVM] setting keyboard hook")
        keyboard.hook(self.keyboard_hook, False)
        print("[SoftKVM] Started!")
        self.menu.start()
        self.window.run() # this is a blocking main loop
        print("[SoftKVM] Closing down")
        self.menu.stop()
        keyboard.unhook_all()

    def about(self):
        webbrowser.open('https://www.clickets.nl/', new=2, autoraise=True)
    
    def switch(self):
        self.window.toggle()
    
    def close(self):
        self.window.hide()
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
        raise argparse.ArgumentTypeError(f"{choice} is not a valid choice ({choices}).")

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
    parser.add_argument("-d", "--display", choices=choices, type=MatchChoices(choices), default=choices[0], help="Choose a display framework")
    choices=['OpenCV', 'pyGame']
    parser.add_argument("-c", "--camera", choices=choices, type=MatchChoices(choices), default=choices[0], help="Choose a camera (hdmi2usb) framework")
    parser.add_argument("-a", "--address", type=MatchIP(), default="127.0.0.1", help="IP address for the SoftKMV-pi")
    args = parser.parse_args()
    
    #debug settings
    #args.camera = 'OpenCV'
    #args.camera = 'pyGame'
    #args.display = 'TK'
    #args.display = 'pyGame'
    #args.address = '192.168.1.76'

    display = None
    match args.camera:
        case 'OpenCV':
            display = display_opencv
        case 'pyGame':
            display = display_pygame
        case _:
            print("Unsupported 'camera' argument. This is probably a bug")
            parser.print_help()
            sys.exit(1)
    window = None
    match args.display:
        case 'TK':
            window = window_tk
        case 'pyGame':
            window = window_tk
        case _:
            print("Unsupported 'display' argument. This is probably a bug")
            parser.print_help()
            sys.exit(1)
    # start main loop
    SoftKVMApp(window, display).run()
    print("[SoftKVM] All done")
