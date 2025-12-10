"""
Detects color user holds against camera using OpenCV
To run: python3 src/color_detector_pkg/color_detector_pkg/color_perception_node.py
"""

import cv2
import numpy as np
from PIL import Image

    # if this doesn't work, double check if webcam number is 0 or a diff num
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open camera")
    exit()
    
while True:
    ret, frame = cap.read()
    width = int(cap.get(3))
    height = int(cap.get(4))

    # Convert BGR to HSV 
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Colors we want to extract
    lower_blue = np.array([90, 50, 50])
    upper_blue = np.array([130, 255, 255])

    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    lower_green = np.array([40, 50, 50])
    upper_green = np.array([80, 255, 255])

    # NOTE we are using a very saturad red, otherwise skin color will pick up
    lower_red1 = np.array([0, 160, 160])
    upper_red1 = np.array([3, 255, 255])
    lower_red2 = np.array([170, 150, 150])
    upper_red2 = np.array([180, 255, 255])

    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)

    colors = {
        'blue': mask_blue,
        'green': mask_green,
        'yellow': mask_yellow,
        'red': mask_red # This is buggy. Need to fix threshold
    }

    for color, (mask) in colors.items():
        # Need to use contour to correctly box the detected color areas
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            # filters out small areas
            if w * h < 500:
                continue

            # Draws the boxes
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.putText(frame, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2) # Puts the color name. Can remove this if not needed, helpful for debugging

    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
    