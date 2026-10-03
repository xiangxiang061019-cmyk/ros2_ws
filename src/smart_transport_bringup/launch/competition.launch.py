from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    use_description = LaunchConfiguration('use_description')
    use_hardware = LaunchConfiguration('use_hardware')
    use_perception = LaunchConfiguration('use_perception')
    use_task = LaunchConfiguration('use_task')
    use_landmarks = LaunchConfiguration('use_landmarks')
    use_map = LaunchConfiguration('use_map')
    map_yaml = LaunchConfiguration('map_yaml')

    description_file = PathJoinSubstitution([
        FindPackageShare('smart_transport_description'),
        'urdf',
        'robot.urdf',
    ])
    params_file = PathJoinSubstitution([
        FindPackageShare('smart_transport_bringup'),
        'config',
        'robot.yaml',
    ])
    robot_description = ParameterValue(Command(['cat ', description_file]), value_type=str)

    actions = [
        DeclareLaunchArgument('use_description', default_value='true'),
        DeclareLaunchArgument('use_hardware', default_value='true'),
        DeclareLaunchArgument('use_perception', default_value='true'),
        DeclareLaunchArgument('use_task', default_value='true'),
        DeclareLaunchArgument('use_landmarks', default_value='true'),
        DeclareLaunchArgument('use_map', default_value='false'),
        DeclareLaunchArgument('map_yaml', default_value=''),
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            condition=IfCondition(use_description),
            output='screen',
        ),
        Node(
            package='smart_transport_hardware',
            executable='ops9_driver',
            name='ops9_driver',
            parameters=[params_file],
            condition=IfCondition(use_hardware),
            output='screen',
        ),
        Node(
            package='smart_transport_hardware',
            executable='lower_driver',
            name='lower_driver',
            parameters=[params_file],
            condition=IfCondition(use_hardware),
            output='screen',
        ),
        Node(
            package='smart_transport_perception',
            executable='qr_detector',
            name='qr_detector',
            parameters=[params_file],
            condition=IfCondition(use_perception),
            output='screen',
        ),
        Node(
            package='smart_transport_perception',
            executable='yolo_detector',
            name='yolo_detector',
            parameters=[params_file],
            condition=IfCondition(use_perception),
            output='screen',
        ),
        Node(
            package='smart_transport_perception',
            executable='radar_obstacle',
            name='radar_obstacle',
            parameters=[params_file],
            condition=IfCondition(use_perception),
            output='screen',
        ),
        Node(
            package='smart_transport_task',
            executable='mission_manager',
            name='mission_manager',
            parameters=[params_file],
            condition=IfCondition(use_task),
            output='screen',
        ),
        Node(
            package='smart_transport_perception',
            executable='competition_landmarks',
            name='competition_landmarks',
            condition=IfCondition(use_landmarks),
            output='screen',
        ),
        Node(
            package='nav2_map_server',
            executable='map_server',
            name='map_server',
            parameters=[{'yaml_filename': map_yaml}],
            condition=IfCondition(use_map),
            output='screen',
        ),
        Node(
            package='nav2_lifecycle_manager',
            executable='lifecycle_manager',
            name='lifecycle_manager_map',
            parameters=[{
                'autostart': True,
                'node_names': ['map_server'],
            }],
            condition=IfCondition(use_map),
            output='screen',
        ),
    ]
    return LaunchDescription(actions)
