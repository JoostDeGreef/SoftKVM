from abc import ABC, abstractmethod

class Window_Interface(ABC):
    #  
    # Create window in hidden state
    #
    @abstractmethod
    def __init__(self, display):
        pass
    
    #
    # Destroy the window
    #
    @abstractmethod
    def __del__(self):
        pass

    #
    # Start the window main loop
    #
    @abstractmethod
    def run(self):
        pass
       
    #
    # Stop the window main loop
    #
    @abstractmethod
    def destroy(self):
        pass
       
    #
    # Make window visible
    #
    @abstractmethod
    def show(self):
        pass

    #
    # Hide window
    #
    @abstractmethod
    def hide(self):
        pass

    #
    # Toggle window visibility
    #
    @abstractmethod
    def toggle(self):
        pass

    #
    # Report window visibility
    #
    @abstractmethod
    def is_visible(self):
        pass
