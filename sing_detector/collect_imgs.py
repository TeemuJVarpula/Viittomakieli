import os

import cv2
from lib.cameraWrapper import Camera


DATA_DIR = "data"
LINE_HEIGHT = 32

command_keys = {
	13 : "enter",
	8 : "backspace",
	32 : "space",
	255 : "delete"
}

if not os.path.exists( DATA_DIR ):
	os.makedirs( DATA_DIR )

chars = "ABCDEFGHIJKLMNOPQRSTUVWXY"
dataset_size = 25

cap = Camera()

def showText( frame, text, pos ):
	cv2.putText( frame, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 1.2, ( 0, 255, 0 ), 1, cv2.LINE_AA )

def collectImages( key ):
	sign = None

	if key in command_keys:
		sign = command_keys[ key ]
	else:
		sign = chr( key )

	singPath = os.path.join( DATA_DIR, sign )

	if not os.path.exists( singPath ):
		os.makedirs( singPath )

	counter = 0

	while counter < dataset_size:
		frame = cap.capture_frame()
		key = cv2.waitKey( 60 )

		if key == 27: # ESC.
			break
		elif key == 32: # Space.
			cv2.imwrite( os.path.join( singPath, "{}.jpg".format( counter ) ), frame )
			counter += 1

		showText( frame, "{}: {}/{}".format( sign, counter, dataset_size ), ( 20, LINE_HEIGHT ) )
		showText( frame, "Press Space to take a picture", ( 20, LINE_HEIGHT * 2 ) )
		showText( frame, "Press Esc to terminate", ( 20, LINE_HEIGHT * 3 ) )
		cv2.imshow( "frame", frame )

while True:
	frame = cap.capture_frame()
	showText( frame, "Press char for letters.", ( 20, LINE_HEIGHT ) )
	showText( frame, "Enter, Backspace, Space or", ( 20, LINE_HEIGHT * 2 ) )
	showText( frame, "Delete for commands.", ( 20, LINE_HEIGHT * 3 ) )
	showText( frame, "Esc to quit.", ( 20, LINE_HEIGHT * 4 ) )
	cv2.imshow( "frame", frame )

	key = cv2.waitKey( 60 )

	if key == 27 or cv2.getWindowProperty('frame',cv2.WND_PROP_VISIBLE) < 1: # ESC or X.
		break
	elif ( ord( chars[0].lower() ) <= key and key <= ord( chars[ len( chars ) - 1 ].lower() ) ) or ( key in command_keys ):
		collectImages( key )

cap.close()
cv2.destroyAllWindows()
