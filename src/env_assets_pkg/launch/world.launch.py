import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    env_assets_dir = get_package_share_directory('env_assets_pkg')
    nav_pkg_dir = get_package_share_directory('nav_pkg')
    world_file = os.path.join(env_assets_dir, 'worlds', 'color_goals.world')
    models_path = os.path.join(env_assets_dir, 'models')

    # Build environment with models path
    current_gz_path = os.environ.get('GZ_SIM_RESOURCE_PATH', '')
    new_gz_path = f"{models_path}:{current_gz_path}" if current_gz_path else models_path
    
    # Copy current environment and update GZ_SIM_RESOURCE_PATH
    env = os.environ.copy()
    env['GZ_SIM_RESOURCE_PATH'] = new_gz_path

    # Launch Gazebo directly with explicit environment
    gazebo_cmd = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_file],
        output='screen',
        env=env
    )

    # Spawn TurtleBot3 using YOUR spawn file from nav_pkg
    spawn_tb3_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav_pkg_dir, 'launch', 'spawn_tb3.launch.py')
        ),
        launch_arguments={
            'x_pose': LaunchConfiguration('x_pose', default='0.0'),
            'y_pose': LaunchConfiguration('y_pose', default='0.0'),
        }.items()
    )

    # Build launch description
    return LaunchDescription([
        gazebo_cmd,
        spawn_tb3_cmd,
    ])