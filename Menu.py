import pystray
import threading

from PIL import Image, ImageDraw

class Menu:
    def _on_clicked(self, icon, item):
        match item.text:
            case 'About':
                if self._on_about:
                    self._on_about()
            case 'Switch':
                if self._on_switch:
                    self._on_switch()
            case 'Exit':
                if self._on_exit:
                    self._on_exit()
    
    def __init__(self, on_exit = None, on_about = None, on_switch = None):
        image = self._create_image(64, 64)
        menu = pystray.Menu(
            pystray.MenuItem(
                'Switch',
                self._on_clicked),
            pystray.MenuItem(
                'About',
                self._on_clicked),
            pystray.MenuItem(
                'Exit',
                self._on_clicked))
        self._icon = pystray.Icon(
            name='SoftKVM',
            title='SoftKVM',
            icon=image,
            menu=menu)
        self._on_exit = on_exit
        self._on_about = on_about
        self._on_switch = on_switch
        self._thread = None
     
    def __del__(self):
        self.stop()
   
    def start(self):
        self._thread = threading.Thread(target=self._icon.run);
        self._thread.daemon = True # make sure the menu thread won't block a clean shutdown
        self._thread.start()

    def stop(self):
        self._on_exit = None
        if self._icon:
            self._icon.stop()
            self._icon = None
        if self._thread:
            self._thread = None
            
    def _create_image(self, width, height):
        # Generate an image and draw a pattern
        background  = (255, 255, 255,   0)
        outline     = (  0,   0,   0, 255)
        fill1       = (192, 192, 192, 255)
        fill2       = (255, 255, 255, 255)
        image = Image.new('RGBA', (width, height), background)
        dx = width // 4
        dy = height // 4
        dc = ImageDraw.Draw(image)        
        dc.rectangle(
            (0, 0, width-dx, height-dy),
            fill=fill1, outline=outline)
        dc.rectangle(
            (dx, dy, width, height),
            fill=fill2, outline=outline)
        return image

