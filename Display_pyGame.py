import pygame.camera

import Display_Interface

class Display_pyGame(Display_Interface.Display_Interface):
    #  
    # initialize display grabber
    #
    def __init__(self):
        pygame.camera.init()
        cameras = pygame.camera.list_cameras()
        self.selected_camera = cameras[0]
        print("Using camera {}".format( self.selected_camera ))
        self.cam = pygame.camera.Camera(self.selected_camera)
        self.width, self.height = [-1,-1]
        self.cam.start()
     
    #
    # Destroy the display grabber
    #
    def __del__(self):
        self.cam.stop()
    
    #
    # grab a frame at the desired size
    #
    def grab_frame(self, width, height):
        if self.width != width or self.height != height:
            self.width, self.height = [width, height]
            self.cam.stop()
            self.cam = pygame.camera.Camera(self.selected_camera, [width, height])
            self.cam.start()
        frame = self.cam.get_image()
        frame = pygame.transform.scale(frame, (width, height))
        return frame

