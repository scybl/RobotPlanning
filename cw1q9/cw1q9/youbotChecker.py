#!/usr/bin/env python3

import sys
import numpy as np
import rclpy
from cw1q9.youbotKineStudent import YoubotKinematicStudent

def main(args=None):
    rclpy.init(args=args)
    node = YoubotKinematicStudent(tf_suffix='student')

    # 期望: ros2 run cw1q9 singularity_checker -- q1 q2 q3 q4 q5 (单位: 度 或 弧度你自己统一)
    if len(sys.argv) != 6:
        node.get_logger().info(
            "Usage: ros2 run cw1q9 singularity_checker -- q1 q2 q3 q4 q5 (in degrees)"
        )
        node.destroy_node()
        rclpy.shutdown()
        return

    try:
        joint_deg = [float(v) for v in sys.argv[1:6]]
    except ValueError:
        node.get_logger().error("All 5 joint values must be numbers.")
        node.destroy_node()
        rclpy.shutdown()
        return

    # 如果你内部都是用弧度，就转成弧度
    joint_rad = [np.deg2rad(v) for v in joint_deg]

    # 用“自己写的” Student 版检查奇异性
    is_singular = node.check_singularity(joint_rad)

    if is_singular:
        node.get_logger().info(f"Joint configuration {joint_deg} deg is SINGULAR.")
    else:
        node.get_logger().info(f"Joint configuration {joint_deg} deg is NOT singular.")

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()