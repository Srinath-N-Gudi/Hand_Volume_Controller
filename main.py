import cv2
import mediapipe as mp
import numpy as np
from ht import find_landmarks
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from pyautogui import press
import time
paused = False
one = False

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
time_normal = time.time()
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():

    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue


    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

    image.flags.writeable = False
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image, points = find_landmarks(image, results)
    if points != []:
        x1, y1 = points[4][1], points[4][2]
        x2, y2 = points[8][1], points[8][2]
        mid_point = (x1+x2)//2, (y1+y2)//2
        cv2.circle(image,(x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(image,(x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(image,mid_point, 10, (255, 0, 255), cv2.FILLED)
        cv2.line(image, (x1, y1), (x2, y2),(255, 0, 255), 2)

        length = math.hypot(x2-x1, y2-y1)
        if length < 50 and not paused:
            
            if not one:
              time_normal = time.time()
              one = True
            cv2.circle(image, ((x1+x2)//2, (y1+y2)//2), 15, (255, 0, 0), cv2.FILLED)
            if time.time() - time_normal > 5:
              press("space")
              paused = True
              
        elif paused and length > 50:
          press("space")
          time_normal = time.time()
          paused = False

        volRange = volume.GetVolumeRange()
        minVol = volRange[0]
        maxVol = volRange[1]

        vol = np.interp(length, [50, 200], [minVol, maxVol])
        if minVol<vol<maxVol:
          volume.SetMasterVolumeLevel(vol, None)

    cv2.imshow('Hand Volume Controller', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
