import cv2
import numpy as np
import mediapipe as mp
import time
import HandTrackingModule as htm
import math
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

ptime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
volrange = volume.GetVolumeRange()
minVol, maxVol = volrange[0], volrange[1]
volBar, vol, volPercent = 400, 0, 0

while cap.isOpened():
    success, img = cap.read()
    img = detector.findhands(img)
    lmlist = detector.findposition(img, draw=False)

    if len(lmlist) != 0:
        print(lmlist[4], lmlist[8])
        x1,y1,x2,y2 = lmlist[4][1], lmlist[4][2], lmlist[8][1], lmlist[8][2]
        cx, cy = (x1+x2)//2, (y1+y2)//2
        cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 15, (255,0,255), cv2.FILLED)
        cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        if length<50: cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

        ## Hand range 50 to 300
        ## Volumne range -65 to 0
        vol = np.interp(length,[50,300], [minVol,maxVol])
        volBar = np.interp(length,[50,300], [400,150])
        volPercent = np.interp(length, [50, 300], [0, 100])
        volume.SetMasterVolumeLevel(vol, None)
        print(vol)

    cv2.rectangle(img,(50,150),(85,400),(0,255,0), 3)
    cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, f'int(volPercent)%', (50, 450), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 0), 4)

    ctime = time.time()
    fps = 1 / (ctime - ptime)
    ptime = ctime

    cv2.putText(img, f"FPS: {int(fps)}", (50, 90), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 4)
    cv2.imshow('img', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        break