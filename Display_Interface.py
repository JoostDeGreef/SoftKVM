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
    @abstractmethod
    def grab_frame(self, width, height):
        pass
