import os
from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node


def generate_launch_description():
    env_assets_dir = get_package_share_directory('env_assets_pkg')
    nav_pkg_dir = get_package_share_directory('nav_pkg')

    world_file = os.path.join(env_assets_dir, 'worlds', 'color_goals.world')
    models_path = os.path.join(env_assets_dir, 'models')

    # Set Gazebo resource path
    current_gz_path = os.environ.get('GZ_SIM_RESOURCE_PATH', '')
    new_gz_path = f"{models_path}:{current_gz_path}" if current_gz_path else models_path

    env = os.environ.copy()
    env['GZ_SIM_RESOURCE_PATH'] = new_gz_path

    # Declare spawn arguments
    declare_x = DeclareLaunchArgument('x_pose', default_value='0.0')
    declare_y = DeclareLaunchArgument('y_pose', default_value='0.0')
    # declare_z = DeclareLaunchArgument('z_pose', default_value='0.05')

    # Launch Gazebo
    gazebo_cmd = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_file],
        output='screen',
        env=env
    )

    # Spawn TurtleBot3
    spawn_tb3_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav_pkg_dir, 'launch', 'spawn_tb3.launch.py')
        ),
        launch_arguments={
            'x_pose': LaunchConfiguration('x_pose'),
            'y_pose': LaunchConfiguration('y_pose'),
            # 'z_pose': LaunchConfiguration('z_pose'),
        }.items()
    )

    # Color perception node
    color_perception_node = Node(
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
    )

    # Controller node
    color_controller_node = Node(
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

    return LaunchDescription([
        declare_x,
        declare_y,
        # declare_z,
        gazebo_cmd,
        spawn_tb3_cmd,
        color_perception_node,
        color_controller_node
    ])