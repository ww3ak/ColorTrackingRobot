"""
Detects color user holds against camera using OpenCV and publishes that color.
To run: python3 src/color_detector_pkg/color_detector_pkg/color_perception_node.py
"""


import cv2
import numpy as np
from PIL import Image
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class DetectsColor(Node):
    def __init__(self):
        super().__init__('color_perception_node')


        self.color_pub = self.create_publisher(String, '/color_detected', 10)
        self.last_color = None
      
        # if this doesn't work, double check if webcam number is 0 or a diff num
        self.declare_parameter('camera_index', 0)
        camera_index = self.get_parameter('camera_index').get_parameter_value().integer_value

        self.cap = cv2.VideoCapture(camera_index, cv2.CAP_V4L2)

        # If camera 0 doesn't work, try others
        if not self.cap.isOpened():
            self.get_logger().warn(f"Camera {camera_index} not available, trying next...")
            for i in range(0, 10):  # Try cameras 0-10
                self.cap = cv2.VideoCapture(i, cv2.CAP_V4L2)
                if self.cap.isOpened():
                    ret, frame = self.cap.read()
                    if ret:
                        camera_index = i
                        break
                    else:
                        self.cap.release()

        if not self.cap.isOpened():
            print("Error: Could not open camera")
            exit()


    def run(self):
            while rclpy.ok():
                ret, frame = self.cap.read()
                if not ret:
                    continue

                color_detected = self.color_detected(frame)

                # Only publish the first detected color once
                if self.last_color is None and color_detected is not None:
                    self.last_color = color_detected
                    msg = String()
                    msg.data = color_detected
                    self.color_pub.publish(msg)
                    print(f"Published detected color: {color_detected}")

                cv2.imshow('Frame', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            self.cap.release()
            cv2.destroyAllWindows()
  
    def color_detected(self, frame):
            best_color = None
            max_area = 0
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Define color masks
            masks = {
                'blue': cv2.inRange(hsv, np.array([90,50,50]), np.array([130,255,255])),
                'green': cv2.inRange(hsv, np.array([40,50,50]), np.array([80,255,255])),
                'yellow': cv2.inRange(hsv, np.array([20,100,100]), np.array([30,255,255])),
                'red': cv2.bitwise_or(
                    cv2.inRange(hsv, np.array([0,160,160]), np.array([3,255,255])),
                    cv2.inRange(hsv, np.array([170,150,150]), np.array([180,255,255]))
                )
            }

            MIN_AREA = 3000  # Ignore small blobs

            for color, mask in masks.items():
                contours,_ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for c in contours:
                    area = cv2.contourArea(c)
                    if area < MIN_AREA:
                        continue

                    if area > max_area:
                        max_area = area
                        best_color = color

                    x, y, w, h = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                    cv2.putText(frame, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            return best_color
        
def main(args=None):
    rclpy.init(args=args)
    node = DetectsColor()
    node.run()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

