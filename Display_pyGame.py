import pygame.camera
import numpy as np

import Display_Interface

class Display_pyGame(Display_Interface.Display_Interface):
    #  
    # initialize display grabber
    #
    def __init__(self, width, height):
        pygame.camera.init()
        cameras = pygame.camera.list_cameras()
        self.selected_camera = cameras[0]
        print("Using camera {}".format( self.selected_camera ))
        self.cam = pygame.camera.Camera(self.selected_camera, [width, height])
        self.cam.start()
        self.width, self.height = [width, height]
     
    #
    # Destroy the display grabber
    #
    def __del__(self):
        self.cam.stop()
    
    #
    # grab a frame at the desired size
    #
    def grab_frame(self, width, height, origin):
        if self.width != width or self.height != height:
            self.cam.stop()
            self.cam = pygame.camera.Camera(self.selected_camera, [width, height])
            self.cam.start()
            self.width, self.height = [width, height]
        frame = self.cam.get_image()
        size = (width, height)
        if origin == Display_Interface.Origin_LT:
            frame = pygame.transform.flip(frame,1,0)
            frame = pygame.transform.rotate(frame,90)
            size = (height, width)
        frame = pygame.transform.smoothscale(frame, size)
        frame = pygame.surfarray.array3d(frame)
        return frame

