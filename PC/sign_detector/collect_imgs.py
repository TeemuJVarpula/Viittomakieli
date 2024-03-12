import os

import cv2

DATA_DIR = "data"
LINE_HEIGHT = 32

if not os.path.exists( DATA_DIR ):
	os.makedirs( DATA_DIR )

chars = "ABCDEFGHIJKLMNOPQRSTUVWXY"
dataset_size = 25

cap = cv2.VideoCapture(0)

def showText( frame, text, pos ):
	cv2.putText( frame, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 1.2, ( 0, 255, 0 ), 1, cv2.LINE_AA )

def collectImages( key ):
	char = chr( key )

	if not os.path.exists( os.path.join( DATA_DIR, char ) ):
		os.makedirs( os.path.join( DATA_DIR, char ) )

	counter = 0

	while counter < dataset_size:
		ret, frame = cap.read()
		showText( frame, "{}: {}/{}".format( char, counter, dataset_size ), ( 20, LINE_HEIGHT ) )
		showText( frame, "Press Space to take a picture", ( 20, LINE_HEIGHT * 2 ) )
		showText( frame, "Press Esc to terminate", ( 20, LINE_HEIGHT * 3 ) )
		cv2.imshow( "frame", frame )

		key = cv2.waitKey( 60 )

		if key == 27: # ESC.
			break
		elif key == ord( " " ): # Space.
			cv2.imwrite( os.path.join( DATA_DIR, char, "{}.jpg".format( counter ) ), frame )
			counter += 1

while True:
	ret, frame = cap.read()
	showText( frame, "Press char to take images", ( 20, 30 ) )
	showText( frame, "Press Esc to quit", ( 20, LINE_HEIGHT * 2 ) )
	cv2.imshow( "frame", frame )

	key = cv2.waitKey( 60 )

	if key == 27: # ESC.
		break
	elif ord( chars[0].lower() ) <= key and key <= ord( chars[ len( chars ) - 1 ].lower() ):
		collectImages( key )

cap.release()
cv2.destroyAllWindows()
