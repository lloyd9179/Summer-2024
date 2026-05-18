import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command

def generate_launch_description():
    gazebo_launch_file = '/home/parallels/ros625/src/my_robot_description/launch/custom_gazebo.launch.py'

    # 获取 URDF 文件路径
    robot_description_config = '/home/parallels/ros625/src/my_robot_description/urdf/robot.urdf'

    # 启动 Gazebo
    gazebo_ros = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch_file),
    )

    # 启动 robot_state_publisher 节点
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': Command(['xacro ', robot_description_config])}]
    )

    # 启动 spawn_entity 节点
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'my_robot', '-file', robot_description_config],
        output='screen'
    )

    return LaunchDescription([
        gazebo_ros,
        robot_state_publisher,
        spawn_entity,
    ])










