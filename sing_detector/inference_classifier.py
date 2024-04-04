import pickle
import numpy as np
from lib.cameraWrapper import Camera
import time
import cv2
import mediapipe as mp

display = None

model_dict = pickle.load( open( './model.p', 'rb' ) )
model = model_dict['model']

cap = Camera()

# Only import display on raspberry.
if cap.raspberry_pi:
	import lib.text_display as display

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands( static_image_mode = True, min_detection_confidence = 0.3 )
chars = "ABCDEFGHIJKLMNOPQRSTUVWXY"
char_dict = {}

take_pic = False
last_command_time = 0

for char in chars:
	char_dict[ char.lower() ] = char

for command in [ "enter", "backspace", "space", "delete" ]:
	char_dict[ command ] = command

recognition_threshold = 30.0 # Lowest acceptable recognition accuracy.
send_frame = 20 # How many frames sign needs to be same before sending.
send_buffer = []
send_buffer_len = 16
accuracy_buff=["L", ":", "0", "0", "%", "_", "_", "_", "_", "_", "_", "R", ":", "0", "0", "%"]
controllhand = "Left"

while True:
	frame = cap.capture_frame()
	frame = cv2.flip(frame,1)
	H, W, _ = frame.shape
	frame_rgb = cv2.cvtColor( frame, cv2.COLOR_BGR2RGB )
	results = hands.process( frame_rgb )
	handlist = []

	if results.multi_hand_landmarks:
		for i in range(0,len(results.multi_hand_landmarks)):
			marks = []
			marks.append(results.multi_hand_landmarks[i])
			hside = results.multi_handedness[i].classification[0].label
			handlist.append( ( hside, marks ) )

		for side, hand in handlist:
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
					x_.append( hand_landmarks.landmark[i].x )
					y_.append( hand_landmarks.landmark[i].y )

				for i in range( len( hand_landmarks.landmark ) ):
					# Move landmarks to upper corner.
					x = hand_landmarks.landmark[i].x - min( x_ )
					y = hand_landmarks.landmark[i].y - min( y_ )

					# Normalize size by scaling landmarks to window height.
					scale = 1 / ( max( y_ ) - min( y_ ) )
					data_aux.append( x * scale )
					data_aux.append( y * scale )
					# print( i, "scale", scale, x * scale, y * scale )

			x1 = int( min( x_ ) * W ) - 10
			y1 = int( min( y_ ) * H ) - 10

			x2 = int( max( x_ ) * W ) + 10
			y2 = int( max( y_ ) * H ) + 10

			prediction = model.predict( [ np.asarray( data_aux ) ] )
			predicted_character = char_dict[ prediction[0] ]
			recognition_accuracy = max( ( model.predict_proba( [ np.asarray( data_aux ) ] ) )[0] ) * 100

			cv2.rectangle( frame, ( x1, y1 ), ( x2, y2 ), ( 220, 220, 220 ), 4 )
			#print(f"rec:{recognition_accuracy}")

			if side == controllhand:
				time_now = time.time()
				take_command = last_command_time == 0 or ( time_now - last_command_time ) > 2
				accuracy_buff[1]=str(recognition_accuracy)[0]
				accuracy_buff[2]=str(recognition_accuracy)[1]
    
				if take_command and recognition_threshold <= recognition_accuracy:
					if predicted_character == "enter":
						take_pic = True
					elif predicted_character in ["backspace", "space", "delete"]:
						if len(send_buffer) > 0:
							if predicted_character == "backspace":
								send_buffer.pop()
							elif predicted_character == "space":
								send_buffer.append("_")
							elif predicted_character == "delete":
								send_buffer.clear()
								print( send_buffer )
					last_command_time = time_now

				cv2.rectangle( frame, ( x1, y1 - 40 ), ( x2, y1 ), ( 220, 220, 220 ),cv2.FILLED)
				cv2.putText( frame, f"{side} {predicted_character} {recognition_accuracy:.0f}%", ( x1, y1 - 10 ), cv2.FONT_HERSHEY_SIMPLEX, 0.7, ( 218,124,110 ), 2, cv2.FILLED )
			else:
				accuracy_buff[13]=str(recognition_accuracy)[0]
				accuracy_buff[14]=str(recognition_accuracy)[1]
				
				if recognition_threshold <= recognition_accuracy:	
					if take_pic == True:		
						send_buffer.append( predicted_character[0][0] )
						take_pic = False

						if send_buffer_len < len( send_buffer ):
							send_buffer.pop(0)

				if recognition_accuracy > recognition_threshold:
					color = ( 242, 202, 134 ) # B,G,R
				else:
					color = ( 0, 0, 255 )

				cv2.rectangle( frame, ( x1, y1 - 40 ), ( x2, y1 ), ( 220, 220, 220 ),cv2.FILLED)
				cv2.putText( frame, f"{side} {predicted_character} {recognition_accuracy:.0f}%", ( x1, y1 - 10 ), cv2.FONT_HERSHEY_SIMPLEX, 0.75, ( 144,203,98 ), 2, cv2.LINE_AA )
				cv2.putText( frame, f"Accuracy: {recognition_accuracy}%", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA )

	if len(send_buffer)>0:
		cv2.putText( frame, "".join( send_buffer ), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (242, 202, 134), 2, cv2.LINE_AA )

	cv2.imshow( 'frame', frame )
	#print(accuracy_buff)
 
	if display != None:
		display.send( send_buffer,accuracy_buff )
		

	if cv2.waitKey( 60 ) == 27: # ESC.
		break
	if cv2.getWindowProperty('frame',cv2.WND_PROP_VISIBLE) < 1:        
		break

cap.close()
cv2.destroyAllWindows()
