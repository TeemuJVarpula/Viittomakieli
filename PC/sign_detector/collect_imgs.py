import os

import cv2

DATA_DIR = './data'

if not os.path.exists( DATA_DIR ):
	os.makedirs( DATA_DIR )

chars = "ABCDEFGHIJKLMNOPQRSTUVWXY"
number_of_classes = len( chars )
dataset_size = 100

cap = cv2.VideoCapture(0)

for j in range( number_of_classes ):
	if not os.path.exists( os.path.join( DATA_DIR, str( j ) ) ):
		os.makedirs( os.path.join( DATA_DIR, str( j ) ) )

	print( 'Collecting data for class {} {}'.format( j, chars[j] ) )

	done = False
	collect = True
	terminate = False

	while True:
		ret, frame = cap.read()
		cv2.putText(frame, "Press 'Q' for: " + str( j ) + " " + chars[j] + ", 'S' to skip" + ", 'E' to exit", ( 20, 50 ), cv2.FONT_HERSHEY_SIMPLEX, 0.8, ( 0, 255, 0 ), 3, cv2.LINE_AA )
		cv2.imshow( 'frame', frame )

		key = cv2.waitKey( 60 )

		if key == ord( 'q' ):
			collect = True
			break
		elif key == ord( 's' ):
			collect = False
			break
		elif key == ord( 'e' ):
			collect = False
			terminate = True
			break

	if collect:
		counter = 0
		while counter < dataset_size:
			ret, frame = cap.read()
			cv2.imshow( 'frame', frame )
			cv2.waitKey( 25 )
			cv2.imwrite( os.path.join( DATA_DIR, str( j ), '{}.jpg'.format( counter ) ), frame )
			counter += 1

	if terminate:
		break

cap.release()
cv2.destroyAllWindows()
