from launch import LaunchDescription
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    pkg = FindPackageShare("vanguard_isaac_control")
    urdf = PathJoinSubstitution([pkg, "urdf", "ur5e_isaac.urdf.xacro"])
    controllers = PathJoinSubstitution([pkg, "config", "controllers.yaml"])
    robot_description = {"robot_description":
        ParameterValue(Command(["xacro ", urdf]), value_type=str)}
    return LaunchDescription([
        Node(package="robot_state_publisher", executable="robot_state_publisher",
             parameters=[robot_description]),
        Node(package="controller_manager", executable="ros2_control_node",
             parameters=[robot_description, controllers], output="screen"),
        Node(package="controller_manager", executable="spawner",
             arguments=["joint_state_broadcaster"]),
        Node(package="controller_manager", executable="spawner",
             arguments=["scaled_joint_trajectory_controller"]),
    ])