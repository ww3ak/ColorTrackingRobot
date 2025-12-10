#!/usr/bin/env python3
"""
Simple webcam using OpenCV
Use this command to run: python3 src/color_detector_pkg/color_detector_pkg/webcam_node.py
"""

import sys
import cv2


def main(source=0):
    try:
        source = int(source)
    except Exception:
        pass

    vid = cv2.VideoCapture(source)
    if not vid.isOpened():
        print(f"ERROR: Could not open video source: {source}")
        return 1

    print("Press 'q' to quit the window")
    while True:
        ret, frame = vid.read()
        if not ret or frame is None:
            print("No frame received — exiting")
            break

        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vid.release()
    cv2.destroyAllWindows()
    return 0


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else 0
    sys.exit(main(src))