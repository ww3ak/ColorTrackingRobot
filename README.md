# Color Tracking Robot Final Project 
Sabrina Simkhovich, Sydney Killilea, Keezhan Hamasoor
CSCI 4511 – Robotics

---

## Build & Run Instructions

1. Ensure **ROS 2** is installed.

2. Navigate to  project workspace:
   ```bash
   cd ColorTrackingRobot
	```
3. Build the workspace:
   ```bash
	colcon build
	```
4. Source the workspace:
   ```bash
	source install/setup.bash
	```
5. Run the program using the launch file:
	```bash
	ros2 launch ros2 launch env_assets_pkg world.launch.py
	```

## Expected Output

After running the program the following output is expected:

1. Web-Cam Appears

2. Gazebo World Launches

3. Burger Robot is spawned and begins making its way toward the detect color.

4. After traveling for a certain time the robot stops near/on target goal in the gazebo world.

## Trouble Shooting

### Could not open camera
1. Unplug camera and replug it back in.

### More than one robot is spawned in the gazebo world
1. Shut down all processes using the commands bash ```pkill -9 -f gazebo```  ```pkill -9 -f ros2```
2. Check if any nodes are still active bash ```ros2 node list```

### When in doubt
1. Remove all build logs and rebuild.