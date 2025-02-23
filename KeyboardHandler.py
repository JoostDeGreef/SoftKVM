import keyboard

from time import time as now

class KeyboardHandler():
    def __init__(self, on_close=None, on_switch=None):
        self._last_ctrl_press = None
        self._last_ctrl_press_count = 0
        self._on_close = on_close
        self._on_switch = on_switch
    
    def __del__(self):
        pass
     
    def start(self):        
        keyboard.hook(self._keyboard_hook, False)
        
    def stop(self):
        keyboard.unhook_all()

    def _keyboard_hook(self, event):
        if event.event_type == 'up':
            match event.name:
                case 'ctrl':
                    if self._last_ctrl_press_count == 0:
                        self._last_ctrl_press = now()
                        self._last_ctrl_press_count = 1
                    elif now() - self._last_ctrl_press < 500:
                        self._last_ctrl_press_count = self._last_ctrl_press_count + 1
                        if self._last_ctrl_press_count >= 3:
                            if self._on_switch:
                                self._on_switch()
                            self._last_ctrl_press = None
                            self._last_ctrl_press_count = 0
                    else:
                        self._last_ctrl_press = now()
                        self._last_ctrl_press_count = 1
                case 'esc':
                    if self._last_ctrl_press_count >= 2 and now() - self._last_ctrl_press < 500:
                        if self._on_close:
                            self._on_close()
                    self._last_ctrl_press = None
                    self._last_ctrl_press_count = 0
                case _:
                    self._last_ctrl_press = None
                    self._last_ctrl_press_count = 0
        else:
            pass
