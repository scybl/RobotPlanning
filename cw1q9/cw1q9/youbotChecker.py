#!/usr/bin/env python3

import sys
import numpy as np
import rclpy
from cw1q9.youbotKineStudent import YoubotKinematicStudent


def main(args=None):
    # 初始化 ROS2
    rclpy.init(args=args)

    # 创建你自己写的 kinematic student 节点（注意：不传 tf_suffix）
    node = YoubotKinematicStudent()
    logger = node.get_logger()

    # 用法：
    #   ros2 run cw1q9 youbot_checker -- q1 q2 q3 q4 q5
    # 这里约定输入单位是：度（degrees）
    if len(sys.argv) != 6:
        logger.info(
            "Usage: ros2 run cw1q9 youbot_checker -- q1 q2 q3 q4 q5 (in degrees)"
        )
        node.destroy_node()
        rclpy.shutdown()
        return

    # 解析命令行参数
    try:
        joint_deg = [float(v) for v in sys.argv[1:6]]
    except ValueError:
        logger.error("All 5 joint values must be numbers.")
        node.destroy_node()
        rclpy.shutdown()
        return

    # 转成弧度，因为你在 kinematics 里用的是弧度
    joint_rad = [np.deg2rad(v) for v in joint_deg]

    # 先用你自己写的 check_singularity
    try:
        is_singular = node.check_singularity(joint_rad)
    except AssertionError:
        # 如果你在 check_singularity 里有 assert 类型检查炸了，这里兜底算一次
        J = node.get_jacobian(joint_rad)
        rank_J = np.linalg.matrix_rank(J, tol=1e-5)
        is_singular = bool(rank_J < 5)

    # 打印奇异性检测结果
    if is_singular:
        logger.info(f"Joint configuration {joint_deg} deg is SINGULAR.")
    else:
        logger.info(f"Joint configuration {joint_deg} deg is NOT singular.")

    # （可选）再打印一下 Jacobian 的奇异值，方便你 debug / 写报告
    try:
        J = node.get_jacobian(joint_rad)
        _, s, _ = np.linalg.svd(J)
        logger.info(f"Jacobian singular values: {s}")
        logger.info(f"Smallest singular value: {s[-1]}")
    except Exception as e:
        logger.warn(f"Could not compute Jacobian singular values: {e}")

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()