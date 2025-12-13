from setuptools import setup

package_name = 'env_assets_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Sabrina',
    maintainer_email='your_email@example.com',
    description='Environment assets for TurtleBot project',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [],
    },
    data_files=[
        # ROS 2 package registration
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Launch files
        ('share/' + package_name + '/launch', ['launch/world.launch.py']),
        # World files
        ('share/' + package_name + '/worlds', ['worlds/color_goals.world']),
        # Model files (list each model SDF and config explicitly)
        ('share/' + package_name + '/models/red_goal', [
            'models/red_goal/model.sdf',
            'models/red_goal/model.config'
        ]),
        ('share/' + package_name + '/models/green_goal', [
            'models/green_goal/model.sdf',
            'models/green_goal/model.config'
        ]),
        ('share/' + package_name + '/models/blue_goal', [
            'models/blue_goal/model.sdf',
            'models/blue_goal/model.config'
        ]),
        ('share/' + package_name + '/models/yellow_goal', [
            'models/yellow_goal/model.sdf',
            'models/yellow_goal/model.config'
        ]),
    ],
)
