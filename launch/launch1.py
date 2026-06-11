import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_path = get_package_share_directory('custom_control_key')
    
    urdf_file = os.path.join(pkg_path, 'urdf', 'robot.urdf')
    ekf_file = os.path.join(pkg_path, 'urdf', 'enc.yaml')
    slam_yaml = os.path.join(pkg_path, 'urdf', 'slam1.yaml')

    # Read URDF Info
    with open(urdf_file, 'r') as inf:
        urdf_info = inf.read()

    # Declare use_sim_time as a Launch Argument (Change default to 'true' if using Gazebo!)
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )
    
    # Grab the configuration reference
    use_sim_time = LaunchConfiguration('use_sim_time')

    # Nav2 Navigation Bringup
    nav2_navigation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('nav2_bringup'), 'launch', 'navigation_launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'params_file': os.path.join(get_package_share_directory('nav2_bringup'), 'params', 'nav2_params.yaml')
        }.items(),
    )

    return LaunchDescription([
        use_sim_time_arg,
        nav2_navigation_launch,

        # Publish Robot State (TF)
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': urdf_info,
                'use_sim_time': use_sim_time
            }]
        ),

        # Publish Joint States
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            parameters=[{'use_sim_time': use_sim_time}]
        ),

        # EKF Sensor Fusion Node (FIXED PARAMETER PASSING)
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[
                ekf_file, 
                {'use_sim_time': use_sim_time}
            ],
            remappings=[
                ('/odometry/filtered', '/odom')
            ]
        ),

        # SLAM Toolbox Node 
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[
                slam_yaml, 
                {'use_sim_time': use_sim_time}
            ]
        )
    ])
