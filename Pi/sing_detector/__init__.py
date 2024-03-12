import cv2
from picamera2 import Picamera2



def init():
      
        piCam = Picamera2()
        piCam.preview_configuration.main.size = (640, 480)
        piCam.preview_configuration.main.format = "RGB888"
        piCam.preview_configuration.align()
        piCam.configure("preview")
        piCam.start()

def capture_frame(self):
        return self.piCam.capture_array()

def close(self):
        self.piCam.close()


#pi_camera.close()
#cv2.destroyAllWindows()

