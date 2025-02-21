import pygame
from pygame.locals import *
import Window_Interface
import cv2
import numpy as np
import os

class Window_pyGame(Window_Interface.Window_Interface):
    #  
    # Create window in hidden state
    #
    def __init__(self, display):
        self.display = display
        # make pyGame (SDL) behave better when desktop scaling enabled
        os.environ["SDL_WINDOWS_DPI_AWARENESS"] = "permonitorv2"
        pygame.init()
        pygame.display.set_caption("SoftKVM")
        self.clock = pygame.time.Clock()
        # pygame.display.set_icon()
        width, height = self.get_size()
        self.screen = pygame.display.set_mode([width, height], flags=pygame.DOUBLEBUF | pygame.FULLSCREEN | pygame.HIDDEN, vsync=True)
    
    #
    # Destroy the window
    #
    def __del__(self):
        pass

    def get_size(self):
        infoObject = pygame.display.Info()
        return infoObject.current_w, infoObject.current_h
        # width, height = pygame.display.get_desktop_sizes()[0]
        # return width, height

    #
    # Start the window main loop
    #
    def run(self):
        while True:
            if pygame.display.get_active():
                width, height = self.get_size()            
                frame = self.display.grab_frame(width, height)
                if not (frame is None):
                    self.screen.fill([0,0,0])
                    if not isinstance(frame, pygame.surface.Surface):
                        frame = np.fliplr(frame)
                        frame = np.rot90(frame)
                        pygame.surfarray.blit_array(self.screen,frame)   
                    else:
                        self.screen.blit(frame, (0,0))
                    pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.SHOWN:
                    width, height = self.get_size()
                    self.screen = pygame.display.set_mode([width, height], flags=pygame.DOUBLEBUF | pygame.FULLSCREEN | pygame.SHOWN, vsync=True)
                elif event.type == pygame.HIDDEN:
                    width, height = self.get_size()
                    self.screen = pygame.display.set_mode([width, height], flags=pygame.DOUBLEBUF | pygame.FULLSCREEN | pygame.HIDDEN, vsync=True)

            self.clock.tick(10)
       
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
