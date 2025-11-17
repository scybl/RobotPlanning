#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import numpy as np
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster
# Import from the other node file within the same ROS 2 package
from cw1q5.cw1q5b_node import forward_kinematics
from geometry_msgs.msg import TransformStamped, Quaternion

"""
This node subscribes to the /joint_states topic, applies the necessary polarity
and offset corrections to the joint angles, computes the forward kinematics for
each joint frame, and publishes the transformations to TF2 for visualization
in RViz.
"""


# ╔════════════════════════════════════════════════════════════════════════╗
# ║           SOLUTION FOR PART 1: DH PARAMETERS & JOINT OFFSETS           ║
# ╚════════════════════════════════════════════════════════════════════════╝
# DH parameters for the youbot arm

youbot_dh_parameters = {'a':    [0.033,     0.155,      0.135,  0,          -0.002],
                        'alpha':[np.pi/2,   0,          0,      -np.pi/2,   0],
                        'd' :   [0.096,     0.019,      0,      0,          0.218],
                        'theta':[0,         np.pi/2,    0,      -np.pi/2,   0]}


# Joint offsets to align the DH model with the URDF representation
deg = np.pi/180
youbot_joint_offsets = [170*deg, 65*deg, -146*deg, 102.5*deg, 167.5*deg]

# Create a new dictionary with the offsets applied to the theta values
youbot_dh_offset_paramters = youbot_dh_parameters.copy()
youbot_dh_offset_paramters['theta'] = [theta + offset for theta, offset in zip(youbot_dh_offset_paramters['theta'], youbot_joint_offsets)]

# Polarity correction for each joint reading
youbot_joint_readings_polarity = [-1, -1, -1, -1, -1]
# ╔════════════════════════════════════════════════════════════════════════╗
# ║                        END OF SOLUTION FOR PART 1                      ║
# ╚════════════════════════════════════════════════════════════════════════╝


def rotmat2q(R):
    """Function for converting a 3x3 Rotation matrix R to quaternion q."""
    q = Quaternion()
    angle = np.arccos((R[0, 0] + R[1, 1] + R[2, 2] - 1) / 2)

    # Use np.isclose for robust floating point comparison
    if np.isclose(angle, 0.0):
        q.w = 1.0
        q.x = 0.0
        q.y = 0.0
        q.z = 0.0
    else:
        xr = R[2, 1] - R[1, 2]
        yr = R[0, 2] - R[2, 0]
        zr = R[1, 0] - R[0, 1]
        norm = np.sqrt(np.power(xr, 2) + np.power(yr, 2) + np.power(zr, 2))
        x = xr / norm
        y = yr / norm
        z = zr / norm
        q.w = np.cos(angle / 2)
        q.x = x * np.sin(angle / 2)
        q.y = y * np.sin(angle / 2)
        q.z = z * np.sin(angle / 2)

    return q


class ForwardKinematicsOffsetNode(Node):
    def __init__(self):
        super().__init__('forward_kinematic_offset_node')
        
        # Initialize the transform broadcaster
        self.br = TransformBroadcaster(self)
        
        # ╔════════════════════════════════════════════════════════════════════════╗
        # ║                     PART 3: INITIALIZE ROS 2 SUBSCRIBER                ║
        # ╚════════════════════════════════════════════════════════════════════════╝
        self.subscription = self.create_subscription(
            JointState,
            'joint_states',
            self.fkine_wrapper,
            10
        )
        self.subscription

        # ╔════════════════════════════════════════════════════════════════════════╗
        # ║                              END OF PART 3                             ║
        # ╚════════════════════════════════════════════════════════════════════════╝

    def fkine_wrapper(self, joint_msg):
        """
        Callback function to compute FK and publish transforms.
        """
        assert isinstance(joint_msg, JointState), "Node must subscribe to a topic where JointState messages are published"
        
        # ╔════════════════════════════════════════════════════════════════════════╗
        # ║                      PART 2: FKINE WRAPPER IMPLEMENTATION              ║
        # ╚════════════════════════════════════════════════════════════════════════╝
        # 关节数量（youbot 5 个关节）
        num_joints = len(youbot_dh_offset_paramters['a'])

        # (1) 取前 num_joints 个关节读数
        raw_readings = list(joint_msg.position[0:num_joints])

        # (2) 极性修正
        corrected_readings = [
            raw * polarity
            for raw, polarity in zip(raw_readings, youbot_joint_readings_polarity)
        ]

        # (3) 使用已经加好 offset 的 DH 参数
        dh_dict = youbot_dh_offset_paramters

        # (4) 逐关节计算 FK 并发布 TF（链式：base_link -> link_1 -> ... -> link_5）
        for i in range(num_joints):

            # base_link → link_(i+1) 的齐次变换
            T_curr = forward_kinematics(
                dh_dict=dh_dict,
                joints_readings=corrected_readings,
                up_to_joint=i + 1
            )

            # base_link → link_i
            if i == 0:
                # link_0 ≡ base_link
                T_prev = np.identity(4)
                parent_frame = 'base_link'
            else:
                T_prev = forward_kinematics(
                    dh_dict=dh_dict,
                    joints_readings=corrected_readings,
                    up_to_joint=i
                )
                parent_frame = f'link_{i}'

            # link_i → link_(i+1)
            T_rel = np.linalg.inv(T_prev) @ T_curr

            # 构造 TF 消息
            transform = TransformStamped()
            transform.header.stamp = self.get_clock().now().to_msg()
            transform.header.frame_id = parent_frame
            transform.child_frame_id = f'link_{i+1}'

            # 平移向量
            transform.transform.translation.x = float(T_rel[0, 3])
            transform.transform.translation.y = float(T_rel[1, 3])
            transform.transform.translation.z = float(T_rel[2, 3])

            # 旋转四元数（由旋转矩阵转为 Quaternion）
            transform.transform.rotation = rotmat2q(T_rel[:3, :3])

            # 发布 TF
            self.br.sendTransform(transform)
        # ╔════════════════════════════════════════════════════════════════════════╗
        # ║                              END OF PART 2                             ║
        # ╚════════════════════════════════════════════════════════════════════════╝


def main(args=None):
    # Standard ROS 2 main function
    rclpy.init(args=args)
    fk_offset_node = ForwardKinematicsOffsetNode()
    rclpy.spin(fk_offset_node)
    
    # Destroy the node explicitly
    fk_offset_node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
