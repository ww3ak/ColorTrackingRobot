"""
Detects color user holds against camera using OpenCV
"""

import cv2
import numpy as np
from PIL import Image

    # if this doesn't work, double check if webcam number is 0 or a diff num
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    # Convert BGR to HSV 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Colors we want to extract
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])

        # lower_yellow = np.array([20, 100, 100])
        # upper_yellow = np.array([30, 255, 255])

        # lower_green = np.array([40, 50, 50])
        # upper_green = np.array([80, 255, 255])

    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
        # mask_green = cv2.inRange(hsv, lower_green, upper_green)
        # mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_ = Image.fromarray(mask)

    box = mask_.getbbox()

    print(box) # prints bounding box if target color is shown
    if box is not None: # This will give us a box around target color
        x1, y1, x2, y2 = box
        frame = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 4)

    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cap.release()
    cv2.destroyAllWindows()
    