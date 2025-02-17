# spot.launch.py
from launch import LaunchDescription
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    # Get package share directory
    pkg_share = FindPackageShare('spot_description')
    
    # Set paths to URDF and xacro files
    xacro_file = PathJoinSubstitution([pkg_share, 'urdf', 'spot.urdf.xacro'])

    # Get robot description from xacro
    robot_description = Command(
        [
            FindExecutable(name='xacro'), ' ',
            xacro_file
        ]
    )

    # Create robot state publisher node
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )

    # Create joint state publisher node
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher'
    )

    # Add Joint State Publisher GUI for testing
    joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui'
    )

    # Return launch description
    return LaunchDescription([
        joint_state_publisher,
        joint_state_publisher_gui,  # This will give you a GUI to move the joints
        robot_state_publisher
    ])