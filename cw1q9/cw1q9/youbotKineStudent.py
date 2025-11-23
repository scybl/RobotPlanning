#!/usr/bin/env python3

import numpy as np
from cw1q9.youbotKineBase import YoubotKinematicBase
import rclpy

class YoubotKinematicStudent(YoubotKinematicBase):
    def __init__(self):
        super().__init__('youbot_kinematic_student', tf_suffix='student')
        # ╔════════════════════════════════════════════════════════════════════════╗
        # ║                   FILL IN the JOINT OFFSETS FOUND IN CW1Q5             ║
        # ╚════════════════════════════════════════════════════════════════════════╝
        # Currently a set of dummy Joint Offsets for YOUR testing
        youbot_joint_offsets = [0.0,
                                np.pi / 2,
                                0.0,
                                -np.pi / 2,
                                0.0]
        # ╔════════════════════════════════════════════════════════════════════════╗
        # ╚════════════════════════════════════════════════════════════════════════╝
        self.dh_params['theta'] = [theta + offset for theta, offset in
                                   zip(self.dh_params['theta'], youbot_joint_offsets)]

        self.youbot_joint_readings_polarity = [-1, 1, 1, 1, 1]

    def forward_kinematics(self, joints_readings, up_to_joint=5):
        T = np.identity(4)
        
        joints_readings = [sign * angle for sign, angle in zip(self.youbot_joint_readings_polarity, joints_readings)]

        for i in range(up_to_joint):
            A = self.standard_dh(self.dh_params['a'][i],
                                 self.dh_params['alpha'][i],
                                 self.dh_params['d'][i],
                                 self.dh_params['theta'][i] + joints_readings[i])
            T = T.dot(A)
            
        return T

    def get_jacobian(self, joint):
        """Given the joint values of the robot, compute the Jacobian matrix. Coursework 1 Question 9a.
        Reference - Lecture 5 slide 24.

        Args:
            joint (list): the state of the robot joints. In a youbot those are revolute

        Returns:
            Jacobian (numpy.ndarray): NumPy matrix of size 6x5 which is the Jacobian matrix.
        """
        assert isinstance(joint, list)
        assert len(joint) == 5

        # ╔════════════════════════════════════════════════════════════════════════╗
        # ║                  YOUR CODE STARTS HERE: CALCULATE JACOBIAN             ║
        # ╚════════════════════════════════════════════════════════════════════════╝
        # For your solution to match the KDL Jacobian, z0 needs to be set [0, 0, -1] instead of [0, 0, 1], since that is how its defined in the URDF.
        # Both are correct.
        
        # Step 1: compute all transforms from base to each joint
        T = np.identity(4)
        joints = [s * q for s, q in zip(self.youbot_joint_readings_polarity, joint)]

        # base axis z0 must be [0,0,-1] for KDL compatibility
        z_axes = [np.array([0, 0, -1])]
        p_positions = [np.array([0, 0, 0])]

        # Forward kinematics to collect z_i and p_i for i = 1..5
        for i in range(5):
            A_i = self.standard_dh(
                self.dh_params['a'][i],
                self.dh_params['alpha'][i],
                self.dh_params['d'][i],
                self.dh_params['theta'][i] + joints[i]
            )
            T = T @ A_i

            # extract rotation Z axis
            z_i = T[0:3, 2]      # axis of current joint in base frame
            p_i = T[0:3, 3]      # position of current joint frame origin

            z_axes.append(z_i)
            p_positions.append(p_i)

        # End effector position pe
        pe = p_positions[-1]

        # Build Jacobian 6x5
        jacobian = np.zeros((6, 5))

        for i in range(5):
            zi = z_axes[i]
            pi = p_positions[i]

            # revolute joint Jacobian
            jacobian[0:3, i] = np.cross(zi, pe - pi)   # linear velocity part
            jacobian[3:6, i] = zi                      # angular velocity part

        # ╔════════════════════════════════════════════════════════════════════════╗
        # ╚════════════════════════════════════════════════════════════════════════╝
        assert jacobian.shape == (6, 5)
        return jacobian

    def check_singularity(self, joint):
        """Check for singularity condition given robot joints. Coursework 1 Question 9c.
        Reference Lecture 5 slide 30.

        Args:
            joint (list): the state of the robot joints. In a youbot those are revolute

        Returns:
            singularity (bool): True if in singularity and False if not in singularity.

        """
        assert isinstance(joint, list)
        assert len(joint) == 5
        
        # ╔════════════════════════════════════════════════════════════════════════╗
        # ║                  YOUR CODE STARTS HERE: CHECK SINGULARITY              ║
        # ╚════════════════════════════════════════════════════════════════════════╝
        # 1. 先用自己写的 get_jacobian 计算当前关节下的雅可比矩阵
        J = self.get_jacobian(joint)

        # 2. 计算雅可比矩阵的秩，5 自由度机械臂如果秩 < 5 则为奇异
        # 设置一个容差避免数值误差造成错误判断
        rank_J = np.linalg.matrix_rank(J, tol=1e-5)

        singularity = bool(rank_J < 5)
        # Your code ends here ------------------------------
        # ╔════════════════════════════════════════════════════════════════════════╗
        # ╚════════════════════════════════════════════════════════════════════════╝
        assert isinstance(singularity, bool)
        return singularity

def main(args=None):
    rclpy.init(args=args)
    node = YoubotKinematicStudent()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()