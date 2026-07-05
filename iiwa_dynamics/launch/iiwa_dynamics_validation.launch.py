#!/usr/bin/env python3

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package='iiwa_dynamics',
                executable='iiwa_dynamics_validator',
                name='iiwa_dynamics_validator',
                output='screen',
            )
        ]
    )
