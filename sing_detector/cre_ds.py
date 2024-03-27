import os
import pickle
import mediapipe as mp
import cv2

# Tuodaan data_normalizer-kirjasto
from data_normalizer import DataNormalizer

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.3)

DATA_DIR = "data"

progress = 1
num_of_files = len(os.listdir(DATA_DIR))

data = []
labels = []

# Alusta DataNormalizer
normalizer = DataNormalizer()

for char in os.listdir(DATA_DIR):
    path = os.path.join(DATA_DIR, char)

    if os.path.isdir(path):
        for img_path in os.listdir(path):
            img = cv2.imread(os.path.join(DATA_DIR, char, img_path))
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img_rgb = cv2.flip(img_rgb, 1)

            # Käsittele kuva käsien havainnointitulosten normalisointiin
            results = hands.process(img_rgb)
            if results.multi_hand_landmarks:  # Detected one hand.
                # Normalisoi data käyttäen DataNormalizeria 
                normalized_data = normalizer.normalize_data(results.multi_hand_landmarks)
                data.append(normalized_data)
                labels.append(char)
            
    print("{}/{}".format(progress, num_of_files))
    progress += 1

f = open("data.pickle", "wb")
pickle.dump({"data": data, "labels": labels}, f)
print("Done")
f.close()
