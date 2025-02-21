from abc import ABC, abstractmethod

class Display_Interface(ABC):
    #  
    # initialize display grabber
    #
    @abstractmethod
    def __init__(self):
        pass
     
    #
    # Destroy the display grabber
    #
    @abstractmethod
    def __del__(self):
        pass
    
    #
    # grab a frame at the desired size
    #
    # TODO: figure out a nice format of image to return, which both TK and pyGame can handle
    @abstractmethod
    def grab_frame(self, width, height):
        pass
