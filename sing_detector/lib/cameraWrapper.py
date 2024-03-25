
import os
import sys
import cv2

class Camera:
	def __init__(self):
		if sys.platform.startswith('linux'):
			if os.uname().machine == "aarch64":
				self.raspberry_pi = True
			else:
				self.raspberry_pi = False
		else:
			self.raspberry_pi = False
		
		if self.raspberry_pi:
			from picamera2 import Picamera2
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
		