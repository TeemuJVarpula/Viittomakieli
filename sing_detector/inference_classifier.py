import pickle
import numpy as np
from lib.cameraWrapper import Camera
import time
import cv2
import mediapipe as mp

COLOR_BGR = ( 30, 30, 30 )
COLOR_TEXT_DEF = ( 200, 200, 200 )
COLOR_GOOD = ( 45, 255, 45 )
COLOR_BAD = ( 45, 45, 255 )

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
send_buffer_len = 16 # Line length.
accuracy_buff=["L", ":", "0", "0", "%", "_", "_", "_", "_", "_", "_", "R", ":", "0", "0", "%"]
controllhand = "Left"

def lerp( a, b, f ):
    return (1 - f) * a + f * b

def colorLerp( a, b, f ):
	return ( lerp( a[0], b[0], f ), lerp( a[1], b[1], f ), lerp( a[2], b[2], f ) )

def drawHandBox( text, pos, acc ):
	textWidth = cv2.getTextSize( text, cv2.FONT_HERSHEY_SIMPLEX, 0.75, 2 )[0][0]
	cv2.rectangle( frame, ( pos[0], pos[1] - 40 ), ( pos[0] + textWidth, pos[1] ), COLOR_BGR, cv2.FILLED )
	cv2.putText( frame, text, ( pos[0], pos[1] - 10 ), cv2.FONT_HERSHEY_SIMPLEX, 0.7, colorLerp( COLOR_BAD, COLOR_GOOD, acc ), 2, cv2.FILLED )

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

			x1 = int( min( x_ ) * W ) - 10
			y1 = int( min( y_ ) * H ) - 10

			x2 = int( max( x_ ) * W ) + 10
			y2 = int( max( y_ ) * H ) + 10

			prediction = model.predict( [ np.asarray( data_aux ) ] )
			predicted_character = char_dict[ prediction[0] ]
			recognition_accuracy = max( ( model.predict_proba( [ np.asarray( data_aux ) ] ) )[0] ) * 100

			cv2.rectangle( frame, ( x1, y1 ), ( x2, y2 ), COLOR_BGR, 4 )

			if side == controllhand:
				time_now = time.time()
				take_command = last_command_time == 0 or ( time_now - last_command_time ) > 2
				accuracy_buff[2]=str(recognition_accuracy)[0]
				accuracy_buff[3]=str(recognition_accuracy)[1]
    
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

					last_command_time = time_now

				drawHandBox( f"{side} {predicted_character} {recognition_accuracy:.0f}%", ( x1, y1 ), recognition_accuracy / 100 )
			else:
				accuracy_buff[13]=str(recognition_accuracy)[0]
				accuracy_buff[14]=str(recognition_accuracy)[1]
				
				if recognition_threshold <= recognition_accuracy:	
					if take_pic == True:		
						send_buffer.append( predicted_character[0][0] )
						take_pic = False

						if send_buffer_len < len( send_buffer ):
							send_buffer.pop(0)

				drawHandBox( f"{side} {predicted_character} {recognition_accuracy:.0f}%", ( x1, y1 ), recognition_accuracy / 100 )

	if len(send_buffer) > 0:
		textSize = cv2.getTextSize( "".join( send_buffer ), cv2.FONT_HERSHEY_SIMPLEX, 1, 2 )[0]
		cv2.rectangle( frame, ( 0, 0 ), ( textSize[0] + 15, 40 ), COLOR_BGR, cv2.FILLED )
		cv2.putText( frame, "".join( send_buffer ), ( 10, 30 ), cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR_TEXT_DEF, 2, cv2.LINE_AA )

	cv2.imshow( 'frame', frame )
 
	if display != None:
		display.send( send_buffer,accuracy_buff )

	if cv2.waitKey( 60 ) == 27 or cv2.getWindowProperty('frame',cv2.WND_PROP_VISIBLE) < 1: # ESC or X.
		break

if display != None:
	display.clear()

cap.close()
cv2.destroyAllWindows()
