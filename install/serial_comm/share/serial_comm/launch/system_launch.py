from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='serial_comm',
            executable='serial_node',
            name='serial_node'
        ),
        Node(
            package='serial_comm',
            executable='user_input_node',
            name='user_input_node'
        ),
        Node(
            package='serial_comm',
            executable='logger_node',
            name='logger_node'
        )
    ])