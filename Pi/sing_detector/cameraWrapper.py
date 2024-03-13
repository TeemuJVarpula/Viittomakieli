
from picamera2 import Picamera2

class PiCamera:
    def __init__(self):
        self.piCam = Picamera2()
        self.piCam.preview_configuration.main.size = (640, 480)
        self.piCam.preview_configuration.main.format = "RGB888"
        self.piCam.preview_configuration.align()
        self.piCam.configure("preview")
        self.piCam.start()

    def capture_frame(self):
        return self.piCam.capture_array()

    def close(self):
        self.piCam.close()
        
      
              
       



