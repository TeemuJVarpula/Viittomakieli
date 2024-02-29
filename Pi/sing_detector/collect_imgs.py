import os

import cv2
from picamera2 import Picamera2

piCam = Picamera2()
piCam.preview_configuration.main.size = ( 640, 480 )
piCam.preview_configuration.main.format = "RGB888"
piCam.preview_configuration.align()
piCam.configure( "preview" )
piCam.start()

DATA_DIR = './data'

if not os.path.exists(DATA_DIR):
	os.makedirs(DATA_DIR)

number_of_classes = 3
dataset_size = 100

for j in range(number_of_classes):
	if not os.path.exists(os.path.join(DATA_DIR, str(j))):
		os.makedirs(os.path.join(DATA_DIR, str(j)))

	print('Collecting data for class {}'.format(j))

	done = False

	while True:
		frame = piCam.capture_array()
		cv2.imshow( "piCam", frame )

		cv2.putText(frame, 'Ready? Press "Q" ! :)', (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3,
					cv2.LINE_AA)
		cv2.imshow('frame', frame)

		if cv2.waitKey(25) == ord('q'):
			break

	counter = 0

	while counter < dataset_size:
		frame = piCam.capture_array()
		cv2.imshow('frame', frame)
		cv2.waitKey(25)
		cv2.imwrite(os.path.join(DATA_DIR, str(j), '{}.jpg'.format(counter)), frame)

		counter += 1

cv2.destroyAllWindows()
