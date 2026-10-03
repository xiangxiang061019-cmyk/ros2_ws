from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    map_yaml = LaunchConfiguration('map_yaml')
    competition_launch = PathJoinSubstitution([
        FindPackageShare('smart_transport_bringup'),
        'launch',
        'competition.launch.py',
    ])
    return LaunchDescription([
        DeclareLaunchArgument('map_yaml', default_value=''),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(competition_launch),
            launch_arguments={
                'use_map': 'true',
                'map_yaml': map_yaml,
                'use_hardware': 'false',
                'use_perception': 'false',
                'use_task': 'false',
                'use_landmarks': 'true',
            }.items(),
        ),
    ])
