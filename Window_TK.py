import ctypes
import cv2
import PIL.Image, PIL.ImageTk
import pygame

from tkinter import *

import Display_Interface
import Window_Interface
import Ticker

class Window_TK(Window_Interface.Window_Interface):
    def __init__(self, display):
        # access to windows system functions
        print("[SoftKVM] Loading user32")
        self.user32 = ctypes.windll.user32
        # initialize the 'camera'
        width, height = self.get_size()
        self.display = display(width, height)
        # update ticker
        self.ticks = Ticker.Ticker()
        # create root window
        self.visible = False
        self.main = Tk()
        self.hide()
        self.main.title("SoftKVM")
        self.main.wm_attributes('-topmost', 'true')
        self.main.wm_attributes('-fullscreen','true')
        self.main.wm_protocol("WM_DELETE_WINDOW", self.onClose)
        # create panel with video output
        self.panel = Label(self.main, highlightthickness=0)
        self.panel.image = None
        self.panel.pack(padx=0, pady=0)
    
    def __del__(self):
        self.display = None

    def run(self):
        self.main.after(10, self.update_image_loop)
        self.main.mainloop()
    
    def onClose(self):
        self.close();

    def destroy(self):
        self.main.destroy()

    def show(self):
        self.visible = True
        self.main.deiconify()
 
    def hide(self):
        self.visible = False
        self.main.withdraw()

    def toggle(self):
        if self.visible:
            self.hide()
        else:
            self.show()

    # move this to an os specific class
    def get_size(self):
        screen_width, screen_height = self.user32.GetSystemMetrics(0), self.user32.GetSystemMetrics(1)
        return screen_width, screen_height

    def display_frame(self):
        width, height = self.get_size()
        frame = self.display.grab_frame(width, height, Display_Interface.Origin_LT)
        if not (frame is None):
            frame = PIL.Image.fromarray(frame)
            frame = PIL.ImageTk.PhotoImage(frame)
        
            self.panel.configure(image=frame)
            self.panel.image = frame 

    def update_image_loop(self):
        if self.visible or (self.ticks() % 100 == 0):
            self.display_frame()
        self.main.after(10, self.update_image_loop)
