import cv2
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
        
def camera_preview():
    piCam = PiCamera()

    try:
        while True:
            frame = piCam.capture_frame()
            cv2.imshow("piCam", frame)

            if cv2.waitKey(1) == ord('q'):
                break
    finally:
        piCam.close()
        cv2.destroyAllWindows()  

camera_preview()        
              
       



