import pickle
import numpy as np

import cv2
import mediapipe as mp
#from picamera2 import Picamera2

from cameraWrapper import PiCamera

piCam = PiCamera()
#piCam.preview_configuration.main.size = ( 640, 480 )
# piCam.preview_configuration.main.size = ( 320, 240 )
#piCam.preview_configuration.main.format = "RGB888"
#piCam.preview_configuration.align()
#piCam.configure( "preview" )
#piCam.start()

model_dict = pickle.load( open( './model.p', 'rb' ) )
model = model_dict['model']

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands( static_image_mode = True, min_detection_confidence = 0.3 )
chars = "ABCDEFGHIJKLMNOPQRSTUVWXY"

last_character = ""
frame_counter = 0
recognition_threshold = 30.0 # Lowest acceptable recognition accuracy.
send_frame = 10 # How many frames sign needs to be same before sending.
send_buffer = []
send_buffer_len = 16

while True:
	data_aux = []
	x_ = []
	y_ = []
	frame = piCam.capture_array()
	H, W, _ = frame.shape
	frame_rgb = cv2.cvtColor( frame, cv2.COLOR_BGR2RGB )
	results = hands.process( frame_rgb )

	if results.multi_hand_landmarks:
		if len( results.multi_hand_landmarks ) == 1:
			for hand_landmarks in results.multi_hand_landmarks:
				mp_drawing.draw_landmarks(
					frame,  # image to draw
					hand_landmarks,  # model output
					mp_hands.HAND_CONNECTIONS,  # hand connections
					mp_drawing_styles.get_default_hand_landmarks_style(),
					mp_drawing_styles.get_default_hand_connections_style()
				)

			for hand_landmarks in results.multi_hand_landmarks:
				for i in range( len( hand_landmarks.landmark ) ):
					x = hand_landmarks.landmark[i].x
					y = hand_landmarks.landmark[i].y

					x_.append( x )
					y_.append( y )

				for i in range( len( hand_landmarks.landmark ) ):
					x = hand_landmarks.landmark[i].x
					y = hand_landmarks.landmark[i].y
					data_aux.append( x - min( x_ ) )
					data_aux.append( y - min( y_ ) )

			x1 = int( min( x_ ) * W ) - 10
			y1 = int( min( y_ ) * H ) - 10

			x2 = int( max( x_ ) * W ) - 10
			y2 = int( max( y_ ) * H ) - 10

			prediction = model.predict( [ np.asarray( data_aux ) ] )
			predicted_character = chars[ int( prediction[0] ) ]
			recognition_accuracy = max( ( model.predict_proba( [ np.asarray( data_aux ) ] ) )[0] ) * 100

			if predicted_character == last_character and recognition_threshold <= recognition_accuracy:
				frame_counter += 1
				if send_frame <= frame_counter:
					send_buffer.append( predicted_character )
					frame_counter = 0

					if send_buffer_len < len( send_buffer ):
						send_buffer.pop(0)
			else:
				frame_counter = 0

			last_character = predicted_character
			color = ( 0, 255, 0 )

			if recognition_accuracy < recognition_threshold:
				color = ( 0, 0, 255 )

			cv2.rectangle( frame, ( x1, y1 ), ( x2, y2 ), ( 0, 0, 0 ), 4 )
			cv2.putText( frame, predicted_character, ( x1, y1 - 10 ), cv2.FONT_HERSHEY_SIMPLEX, 1.3, ( 0, 255, 0 ), 3, cv2.LINE_AA )
			cv2.putText( frame, f"Accuracy: {recognition_accuracy:.2f}% Frame: {frame_counter}/{send_frame}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA )
	else:
		frame_counter = 0

	cv2.putText( frame, "".join( send_buffer ), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA )
	cv2.imshow( "piCam", frame )

	if cv2.waitKey( 60 ) == 27: # ESC.
		break

piCam.close()
cv2.destroyAllWindows()
