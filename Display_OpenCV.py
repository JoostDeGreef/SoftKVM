from abc import ABC, abstractmethod
import cv2

import Display_Interface

class Display_OpenCV(Display_Interface.Display_Interface):
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW) # CAP_ANY?
        if not self.video_capture.isOpened():
            print("Could not open any camera")
            exit(1)

        self.width, self.height = [-1, -1]
                  
    def __del__(self):
        self.video_capture.release()
        
    def grab_frame(self, width, height):   
        if self.video_capture.isOpened():
            if width != self.width or height != self.height:                    
                self.width, self.height = width, height
                self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
                self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

            ret, frame = self.video_capture.read()

            if ret:
                frame_height, frame_width, _ = frame.shape

                scaleWidth = float(self.width)/float(frame_width)
                scaleHeight = float(self.height)/float(frame_height)
            
                frame = cv2.resize(frame,None,fx=scaleWidth,fy=scaleHeight,interpolation=cv2.INTER_CUBIC)
                return frame
            
            return None
