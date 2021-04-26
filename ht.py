import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

def find_landmarks(image, results, draw=True):
    points = []
    if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                if draw:
                    mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                for id, lm in enumerate(hand_landmarks.landmark):
                    h,w,c = image.shape
                    cx , cy = int(lm.x *w), int(lm.y*h)
                    points.append((id, cx, cy))
    return image, points