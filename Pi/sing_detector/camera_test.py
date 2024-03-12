import cv2
#from picamera2 import Picamera2

import __init__ as camera
    
piCam = camera.init()

    
#piCam = PiCamera()
#piCam.preview_configuration.main.size = ( 640, 480 )
#piCam.preview_configuration.main.format = "RGB888"
#piCam.preview_configuration.align()
#piCam.configure( "preview" )
#piCam.start()

while True:
	frame = piCam.capture_array()
	cv2.imshow( "piCam", frame )

	if cv2.waitKey( 1 ) == ord( 'q' ):
		break

piCam.close()
cv2.destroyAllWindows()
