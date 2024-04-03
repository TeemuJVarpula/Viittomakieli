import os
import pickle

import mediapipe as mp
import cv2
import matplotlib.pyplot as plt

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands( static_image_mode = True, max_num_hands=1 , min_detection_confidence = 0.3 )

DATA_DIR = "data"

progress = 1
num_of_files = len( os.listdir( DATA_DIR ) )

data = []
labels = []

for char in os.listdir( DATA_DIR ):
	path = os.path.join( DATA_DIR, char )

	if os.path.isdir( path ):
		for img_path in os.listdir( path ):
			
			img = cv2.imread( os.path.join( DATA_DIR, char, img_path ) )
			img_rgb = cv2.cvtColor( img, cv2.COLOR_BGR2RGB )
			img_rgb = cv2.flip( img_rgb, 1 )
   
			data_aux = []
			x_ = []
			y_ = []
			results = hands.process( img_rgb )

			if results.multi_hand_landmarks: # Detected one hand.
				for hand_landmarks in results.multi_hand_landmarks:
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

				data.append( data_aux )
				labels.append( char )
				
	print( "{}/{}".format( progress, num_of_files ) )
	progress += 1

f = open( "data.pickle", "wb" )
pickle.dump( { "data": data, "labels": labels }, f )
print("Done")
f.close()
