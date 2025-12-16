from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='color_detector_pkg',
            executable='color_perception_node',
            name='color_detector',
            output='screen',
            parameters=[{
                'camera_index': 0,
                'camera_topic': '/camera/image_raw',
                'detection_color': 'red',
                'detection_threshold': 0.5
            }]
        ),
        Node(
            package='color_detector_pkg',
            executable='color_controller',
            name='color_controller',
            output='screen',
            parameters=[{
                'color_topic': '/color_detected',
                'cmd_topic': '/cmd_vel',
                'max_linear_speed': 0.5,
                'angular_gain': 1.0
            }]
        )
    ])