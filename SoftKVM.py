# pip install opencv-python
# pip install keyboard
# pip install pillow
import keyboard
import threading

from Display_OpenCV import Display_OpenCV as OpenCV
import Window_TK

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
            
if __name__ == '__main__':
    print("[SoftKVM] Starting")
    # create display grabber
    display = OpenCV()    
    # create main window (hidden)
    print("[SoftKVM] Creating main window")
    window = Window_TK.Window_TK(display)
    # start main loop
    SoftKVMApp(window).run()
    print("[SoftKVM] All done")
