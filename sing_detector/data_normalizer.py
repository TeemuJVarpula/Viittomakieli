import os
import pickle
import cv2
import matplotlib.pyplot as plt

class DataNormalizer:
    def __init__(self):
        self.data_aux = []

    def crop_to_palm_size(self, image, hand_landmarks, results):  # Lisätty 'results' argumentti
        # Toteuta kuvan rajaus kämmenen kokoiseksi tässä
        x_ = []  # Lisätty listat x_ ja y_
        y_ = []

        cropped_image = None  # Määrittele cropped_image

        if results.multi_hand_landmarks:  # Havaitaan yksi käsi.
            for hand_landmarks in results.multi_hand_landmarks:
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y

                    x_.append(x)
                    y_.append(y)

                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    self.data_aux.append(x - min(x_))
                    self.data_aux.append(y - min(y_))

                # Palauta rajattu kuva
                cropped_image = image[min(y_):max(y_), min(x_):max(x_)]  # Rajaa kuva kämmenen kokoiseksi

        return cropped_image

    def normalize_data(self, hand_landmarks):
            # Etsi kämmen (landmark[0]) ja keskisormen päässä oleva landmark (landmark[12])
            palm_landmark = hand_landmarks.landmark[0]
            middle_finger_tip_landmark = hand_landmarks.landmark[12]

            # Laske kämmenestä keskisormen päähän oleva etäisyys
            palm_middle_finger_distance_x = middle_finger_tip_landmark.x - palm_landmark.x
            palm_middle_finger_distance_y = middle_finger_tip_landmark.y - palm_landmark.y

            # Käy läpi kaikki käsien landmarkit
            for landmark in hand_landmarks.landmark[1:]:
                # Laske etäisyys x- ja y-akseleilla kämmenestä kyseiseen pisteeseen
                distance_x = landmark.x - palm_landmark.x
                distance_y = landmark.y - palm_landmark.y
                    
                # Normalisoi etäisyydet käyttäen kämmenestä keskisormen päähän olevaa etäisyyttä
                relative_distance_x = abs(distance_x / palm_middle_finger_distance_x)
                relative_distance_y = abs(distance_y / palm_middle_finger_distance_y)

                # Lisää suhteelliset etäisyydet dataan
                self.data_aux.append(relative_distance_x)
                self.data_aux.append(relative_distance_y)

            # Tulosta suhteelliset etäisyydet
            #print("All relative distances X:", self.data_aux[::2])  # Tulosta x-akselin etäisyydet
            #print("First 10 relative distances Y:", self.data_aux[1:21:2])

            # Palauta suhteelliset etäisyydet
            return self.data_aux
