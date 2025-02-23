import pygame
from pygame.locals import *
import Display_Interface
import Window_Interface

class Window_pyGame(Window_Interface.Window_Interface):
    #  
    # Create window in hidden state
    #
    def __init__(self, display):
        pygame.init()
        pygame.display.set_caption("SoftKVM")
        self.clock = pygame.time.Clock()
        # pygame.display.set_icon()
        width, height = self.get_size()
        self.display = display(width, height)
        self.screen = pygame.display.set_mode([width, height], flags=pygame.DOUBLEBUF | pygame.FULLSCREEN | pygame.HIDDEN, vsync=True)
    
    #
    # Destroy the window
    #
    def __del__(self):
        self.display = None

    def get_size(self):
        infoObject = pygame.display.Info()
        return infoObject.current_w, infoObject.current_h

    #
    # Start the window main loop
    #
    def run(self): 
        while True:
            if pygame.display.get_active():
                width, height = self.get_size()            
                frame = self.display.grab_frame(width, height, Display_Interface.Origin_LB)
                if not (frame is None):
                    self.screen.fill([0,0,0])
                    pygame.surfarray.blit_array(self.screen,frame)   
                    pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.SHOWN:
                    width, height = self.get_size()
                    pygame.mouse.set_visible(False)
                    self.screen = pygame.display.set_mode([width, height], flags=pygame.DOUBLEBUF | pygame.FULLSCREEN | pygame.SHOWN, vsync=True)
                elif event.type == pygame.HIDDEN:
                    width, height = self.get_size()
                    pygame.mouse.set_visible(True)
                    self.screen = pygame.display.set_mode([width, height], flags=pygame.DOUBLEBUF | pygame.FULLSCREEN | pygame.HIDDEN, vsync=True)

            self.clock.tick(10)
       
    def is_visible(self):
        return pygame.display.get_active()

    #
    # Stop the window main loop
    #
    def destroy(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
       
    #
    # Make window visible
    #
    def show(self):
        pygame.event.post(pygame.event.Event(pygame.SHOWN))
    
    #
    # Hide window
    #
    def hide(self):
        pygame.event.post(pygame.event.Event(pygame.HIDDEN))

    #
    # Toggle window visibility
    #
    def toggle(self):
        if pygame.display.get_active():
            self.hide()
        else:
            self.show()
