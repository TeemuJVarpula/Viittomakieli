import platform
import os
import cv2
from picamera2 import Picamera2


class Camera:
    def __init__(self):
        self.raspberry_pi = platform.system() == 'Linux' and os.uname().machine == "arm"
        if self.raspberry_pi:
            self.camera = Picamera2()
            self.camera.preview_configuration.main.size = (640, 480)
            self.camera.preview_configuration.main.format = "RGB888"
            self.camera.preview_configuration.align()
            self.camera.configure("preview")
            self.camera.start()
        else:
            self.camera = cv2.VideoCapture(0)

    def capture_frame(self):
        if self.raspberry_pi:
            return self.camera.capture_array()
        else:
            ret,frame = self.camera.read()
            return frame
    

    def close(self):
        if self.raspberry_pi:
            self.camera.close() 
        else: 
            self.camera.release()
        
#cv camera
#platform library 


