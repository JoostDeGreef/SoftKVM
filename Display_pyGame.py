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
        frame = pygame.transform.scale(frame, (width, height))
        frame = pygame.surfarray.array3d(frame)
        if origin == Display_Interface.Origin_LT:
            frame = np.fliplr(frame)
            frame = np.rot90(frame)
        return frame

