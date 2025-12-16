import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/killi167/CSCI4551 Final Project/ColorTrackingRobot/install/color_detector_pkg'
