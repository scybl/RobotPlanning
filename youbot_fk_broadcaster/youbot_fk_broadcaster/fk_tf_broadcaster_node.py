#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import numpy as np
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster
from geometry_msgs.msg import TransformStamped, Quaternion

"""
This node subscribes to the /joint_states topic, applies the necessary polarity
and offset corrections to the joint angles, computes the forward kinematics for
each joint frame, and publishes the transformations to TF2 for visualization
in RViz.
"""


youbot_dh_parameters = {'a':    [0.033,     0.155,      0.135,  0,          -0.002],
                        'alpha':[np.pi/2,   0,          0,      -np.pi/2,   0],
                        'd' :   [0.147,     0.019,      0,      0,          0.185],
                        'theta':[0,         np.pi/2,    0,      -np.pi/2,   0]}

deg = np.pi/180
youbot_joint_offsets = [170*deg, 65*deg, -146*deg, 102.5*deg, 167.5*deg]

youbot_dh_offset_paramters = youbot_dh_parameters.copy()
youbot_dh_offset_paramters['theta'] = [theta + offset for theta, offset in zip(youbot_dh_offset_paramters['theta'], youbot_joint_offsets)]

youbot_joint_readings_polarity = [-1, -1, -1, -1, -1]


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


def standard_dh(a, alpha, d, theta):
    """Return the standard Denavit-Hartenberg transform for one link."""
    return np.array([
        [np.cos(theta), -np.sin(theta)*np.cos(alpha),  np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
        [np.sin(theta),  np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
        [0.0,            np.sin(alpha),                np.cos(alpha),               d],
        [0.0,            0.0,                          0.0,                         1.0],
    ])


def forward_kinematics(dh_dict, joints_readings, up_to_joint=5):
    """Multiply DH transforms from the base to the selected YouBot joint."""
    T = np.identity(4)
    for i in range(up_to_joint):
        T = T.dot(standard_dh(
            a=dh_dict['a'][i],
            alpha=dh_dict['alpha'][i],
            d=dh_dict['d'][i],
            theta=dh_dict['theta'][i] + joints_readings[i],
        ))
    return T


class ForwardKinematicsOffsetNode(Node):
    def __init__(self):
        super().__init__('youbot_fk_tf_broadcaster')
        
        # Initialize the transform broadcaster
        self.br = TransformBroadcaster(self)
        
        self.subscription = self.create_subscription(
            JointState,
            'joint_states',
            self.fkine_wrapper,
            10
        )
        self.subscription

    def fkine_wrapper(self, joint_msg):
        """
        Callback function to compute FK and publish transforms.
        """
        assert isinstance(joint_msg, JointState), "Node must subscribe to a topic where JointState messages are published"

        num_joints = len(youbot_dh_offset_paramters['a'])

        raw_readings = list(joint_msg.position[0:num_joints])

        # change the direction
        corrected_readings = [
            raw * polarity
            for raw, polarity in zip(raw_readings, youbot_joint_readings_polarity)
        ]

        dh_dict = youbot_dh_offset_paramters

        # Iterate over all joints
        for i in range(num_joints):

            # base_link → link_(i+1)
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

            transform = TransformStamped()
            transform.header.stamp = self.get_clock().now().to_msg()
            transform.header.frame_id = parent_frame
            transform.child_frame_id = f'link_{i+1}'

            transform.transform.translation.x = float(T_rel[0, 3])
            transform.transform.translation.y = float(T_rel[1, 3])
            transform.transform.translation.z = float(T_rel[2, 3])

            transform.transform.rotation = rotmat2q(T_rel[:3, :3])

            self.br.sendTransform(transform)


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
