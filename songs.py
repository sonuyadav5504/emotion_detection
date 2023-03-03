import cv2
import numpy as np
import time
import mediapipe as mp
from keras.models import load_model
from playsound import playsound

model = load_model("model.h5")
label = np.load("labels.npy")
hol = mp.solutions.holistic
h = hol.Holistic()
drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

j = 0
p = ""

while j <= 40:
    lst = []
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    res = h.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if res.face_landmarks:
        for i in res.face_landmarks.landmark:
            lst.append(i.x - res.face_landmarks.landmark[1].x)
            lst.append(i.y - res.face_landmarks.landmark[1].y)
        lst = np.array(lst).reshape(1, -1)
        p = label[np.argmax(model.predict(lst))]

    j = j+1
    cv2.putText(frame, p, (50, 50), cv2.FONT_ITALIC, 1, (255, 0, 0), 2)
    cv2.imshow("window", frame)
    k = cv2.waitKey(25)
    if k == ord('q'):
        break

print("Hey!")
print("Currently your emotion is " + p +".")
print("Now Music is Playing based on your emotion, within  2 seconds~")
cv2.destroyAllWindows()
cap.release()
time.sleep(2)
playsound(p+".mp3")