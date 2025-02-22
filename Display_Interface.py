from abc import ABC, abstractmethod

Origin_LT = 1 # left top
Origin_LB = 2 # left bottom

class Display_Interface(ABC):
    #  
    # initialize display grabber
    #
    @abstractmethod
    def __init__(self, width, height):
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
    # return np.ndarray with the image in the desired orientation
    # 
    @abstractmethod
    def grab_frame(self, width, height, origin=Origin_LT):
        pass
