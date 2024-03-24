import cv2
import numpy as np
import mediapipe as mp
import time

print(mp.__version__)
print(cv2.__version__)
class handDetector():
    def __init__(self, mode=False, maxHands=2, detectionCon=False, complexity=1, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.complexity = complexity
        self.trackCon = trackCon

        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpdraw = mp.solutions.drawing_utils

    def findhands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:
                if draw: self.mpdraw.draw_landmarks(img, handlms, self.mphands.HAND_CONNECTIONS)
        return img

    def findposition(self, img, handNo=0, draw=True):
        lmlist = []
        if self. results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h,w,c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                # print(id, cx, cy)
                lmlist.append([id, cx, cy])
                # way to identify the specific point out of all the 20 points
                if draw: cv2.circle(img, (cx,cy), 10, (255,0,255), cv2.FILLED)

        return lmlist

def main():
    ptime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while cap.isOpened():
        success, img = cap.read()
        img = detector.findhands(img)
        lmlist = detector.findposition((img))
        if len(lmlist)!=0: print(lmlist[4])

        ctime = time.time()
        fps = 1 / (ctime - ptime)
        ptime = ctime

        cv2.putText(img, f"FPS: {int(fps)}", (50, 90), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 255), 4)
        cv2.imshow('img', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break


# if __name__ == "__main__":
#     main()