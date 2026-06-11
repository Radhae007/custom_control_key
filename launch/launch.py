import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_path = get_package_share_directory('custom_control_key')
    urdf_file = os.path.join(pkg_path, 'urdf', 'robot.urdf')
    world_file = os.path.join(pkg_path, 'worlds', 'obstacle.world')
    ekf_file = os.path.join(pkg_path, 'urdf', 'ekf.yaml')
    slam_yaml = os.path.join(pkg_path, 'urdf', 'slam1.yaml')
    # global_costmap_params=os.path.join(pkg_path,'urdf','global_costmap_params.yaml')
    # local_costmap_params=os.path.join(pkg_path,'urdf','local_costmap_params.yaml')
    # amcl_file = os.path.join(pkg_path, 'urdf', 'amcl.yaml')
    map_file = os.path.join(pkg_path, 'maps', 'my_saved_map.pgm')

    # # Check if URDF file exists
    # print(f"Checking URDF file path: {urdf_file}")
    # if not os.path.exists(urdf_file):
    #     print('URDF file not found!')
    # else:
    #     print('URDF file found.')

    # # Check other files
    # print(f"Checking EKF file path: {ekf_file}")
    # if not os.path.exists(ekf_file):
    #     print('EKF file not found!')
    # else:
    #     print('EKF file found.')
    
    # print(f"Checking SLAM file path: {slam_yaml}")
    # if not os.path.exists(slam_yaml):
    #     print('SLAM YAML file not found!')
    # else:
    #     print('SLAM YAML file found.')

    # print(f"Checking AMCL file path: {amcl_file}")
    # if not os.path.exists(amcl_file):
    #     print('AMCL file not found!')
    # else:
    #     print('AMCL file found.')

    # print(f"Checking MAP file path: {map_file}")
    # if not os.path.exists(map_file):
    #     print('MAP file not found!')
    # else:
    #     print('MAP file found.')

    with open(urdf_file, 'r') as inf:
        urdf_info = inf.read()

    # 1. Start Gazebo using the official ROS 2 wrapper
    # gazebo = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
    #     ),
    #     launch_arguments={'world': world_file}.items()
    # )
    nav2_navigation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('nav2_bringup'), 'launch', 'navigation_launch.py')),
        launch_arguments={
            'use_sim_time': 'false',
            'params_file': os.path.join(get_package_share_directory('nav2_bringup'), 'params', 'nav2_params.yaml')
        }.items(),
    )

    return LaunchDescription([
        # Start Gazebo  
        # gazebo,
        nav2_navigation_launch,
        # nav2_bringup_launch,

        # Publish Robot State (TF)
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': urdf_info,
                'use_sim_time': False  
            }]
        ),

        # Publish Joint States
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            parameters=[{'use_sim_time': False}]
        ),

        # Spawn Robot into Gazebo
#        Node(
#            package='gazebo_ros',
#            executable='spawn_entity.py',
#            output='screen',
#            arguments=[
#                '-topic', 'robot_description', 
#                '-entity', 'my_mobile_robot',
#                '-x', '0.9', 
#                '-y', '0.6', 
#                '-z', '0.1'
#            ]
#        ),

        # EKF Sensor Fusion Node
#        Node(
 #           package='robot_localization',
  #          executable='ekf_node',
   #         name='ekf_filter_node',
    #        output='screen',
     #       parameters=[ekf_file, {'use_sim_time': False}],
      #      remappings=[
       #         ('/odometry/filtered', '/odom')
        #    ]
       # ),

        # SLAM Toolbox Node (Disabled to use Nav2)
        Node(
            package='slam_toolbox',
            executable='async_slam_toolbox_node',
            name='slam_toolbox',
            output='screen',
            parameters=[slam_yaml, {'use_sim_time': False}]
        )
        # Node(
        #     package='teleop_twist_keyboard',
        #     executable='teleop_twist_keyboard',
        #     name='key_control',
        #     output='screen',
        #     parameters=[{'use_sim_time':True}]
        # ),

        #AMCL IS NEEDED ONLY AFTER MAPPING OF AN UNKNOWN TERRAIN IS DONE 
        # Node(
        #     package='nav2_amcl',
        #     executable='amcl',
        #     name='amcl',
        #     output='screen',
        #     parameters=[
        #         {'use_sim_time': True},
        #         {'amcl': amcl_file}
        #     ]
        # )
        # #The nav2 has a prebuilt launch file , which will launch every needed compenent like (nav2_brinup, move_base etc )
        # Node(
        #     package='nav2_bringup',
        #     executable='bringup_node',
        #     output='screen',
        #     parameters=[{'use_sim_time': True}],
        #     remappings=[
        #         ('/map', '/dynamic_map')  # If you are dynamically updating the map
        #     ]
        # ),
    ])
