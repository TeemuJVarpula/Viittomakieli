class DataNormalizer:
    def __init__(self):
        self.data_aux = []

    def normalize_data(self, hand_landmarks):
        if hand_landmarks:
            for hand_landmark in hand_landmarks:
                # Määritä vertailupiste landmarkin indeksi 0 avulla
                reference_landmark = hand_landmark.landmark[0]
                for landmark in hand_landmark.landmark[1:]:
                    # Laske etäisyys landmarkin indeksi 0 suhteessa
                    distance_x = landmark.x - reference_landmark.x
                    distance_y = landmark.y - reference_landmark.y
                    self.data_aux.append(distance_x)
                    self.data_aux.append(distance_y)

        return self.data_aux
