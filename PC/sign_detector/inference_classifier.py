import pickle
import numpy as np
import time
import cv2
import mediapipe as mp

model_dict = pickle.load( open( './model.p', 'rb' ) )
model = model_dict['model']

cap = cv2.VideoCapture( 0 )

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands( static_image_mode = True, min_detection_confidence = 0.3 )
chars = "ABCDEFGHIJKLMNOPQRSTUVWXY"

take_pic=False
last_pictime=0
recognition_threshold = 30.0 # Lowest acceptable recognition accuracy.
send_frame = 20 # How many frames sign needs to be same before sending.
send_buffer = []
send_buffer_len = 16
controllhand="Left"

while True:

	ret, frame = cap.read()
	frame=cv2.flip(frame,1)
	H, W, _ = frame.shape
	frame_rgb = cv2.cvtColor( frame, cv2.COLOR_BGR2RGB )
	results = hands.process( frame_rgb )

	if results.multi_hand_landmarks:
		handlist=[]
		
		for i in range (0,len(results.multi_hand_landmarks)):
			marks=[]	
			marks.append(results.multi_hand_landmarks[i])
			hside=results.multi_handedness[i].classification[0].label
			handlist.append((hside,marks))

		for side,hand in handlist:
			data_aux = []
			x_ = []
			y_ = []
		
			for hand_landmarks in hand:
				mp_drawing.draw_landmarks(
					frame,  # image to draw
					hand_landmarks,  # model output
					mp_hands.HAND_CONNECTIONS,  # hand connections
					mp_drawing_styles.get_default_hand_landmarks_style(),
					mp_drawing_styles.get_default_hand_connections_style()
				)

			for hand_landmarks in hand:
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

			cv2.rectangle( frame, ( x1, y1 ), ( x2, y2 ), ( 0, 0, 0 ), 4 )

			if  side == controllhand:
				now=0
				if predicted_character == "A":
					if take_pic == False:
						now=time.time()
						if last_pictime	== 0:
							take_pic = True
							last_pictime=now
							print(f"pic1 {now}")
						elif now-last_pictime > 2:
							print(f"pic {now}")
							last_pictime=now
							take_pic = True
	
				cv2.putText( frame, f"{side} {predicted_character} {recognition_accuracy}", ( x1, y1 - 10 ), cv2.FONT_HERSHEY_SIMPLEX, 1.3, ( 0, 255, 0 ), 3, cv2.LINE_AA )
		
			else:
				if take_pic == True:
					if recognition_threshold <= recognition_accuracy:
						send_buffer.append( predicted_character )
						take_pic = False

						if send_buffer_len < len( send_buffer ):
							send_buffer.pop(0)

				if recognition_accuracy > recognition_threshold:
					color = ( 242, 202, 134 ) #B,G,R
				else:
					color = ( 0, 0, 255 )

				cv2.putText( frame, f"{side} {predicted_character} {recognition_accuracy}", ( x1, y1 - 10 ), cv2.FONT_HERSHEY_PLAIN, 1.3, ( 0, 255, 0 ), 3, cv2.LINE_AA )
				cv2.putText( frame, f"Accuracy: {recognition_accuracy}%", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA )
 
	cv2.putText( frame, "".join( send_buffer ), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA )
	cv2.imshow( 'frame', frame )

	if cv2.waitKey( 60 ) == 27: # ESC.
		break

cap.release()
cv2.destroyAllWindows()

1710333814.8876731
1710333814.7461472