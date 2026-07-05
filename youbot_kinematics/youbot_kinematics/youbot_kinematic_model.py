#!/usr/bin/env python3

import numpy as np
from youbot_kinematics.youbotKineBase import YoubotKinematicBase
import rclpy

class YoubotKinematicModel(YoubotKinematicBase):
    def __init__(self):
        super().__init__('youbot_kinematic_model', tf_suffix='model')
        # Joint offsets align DH coordinates with the YouBot URDF conventions.
        deg = np.pi/180
        youbot_joint_offsets = [170*deg, 65*deg, -146*deg, 102.5*deg, 167.5*deg]
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
        """Given the joint values of the robot, compute the YouBot Jacobian matrix.
        Reference - Lecture 5 slide 24.

        Args:
            joint (list): the state of the robot joints. In a youbot those are revolute

        Returns:
            Jacobian (numpy.ndarray): NumPy matrix of size 6x5 which is the Jacobian matrix.
        """
        assert isinstance(joint, list)
        assert len(joint) == 5

        # For your solution to match the KDL Jacobian, z0 needs to be set [0, 0, -1] instead of [0, 0, 1], since that is how its defined in the URDF.
        # Both are correct.

        # Step 1: collect z_i and p_i using the existing forward_kinematics method
        # base frame (i = 0)
        z_axes = [np.array([0, 0, -1])]   # z0 defined as in the comment above
        p_positions = [np.array([0, 0, 0])]

        # use forward_kinematics to get transforms from base to each joint frame i = 1..5
        for i in range(1, 6):
            T = self.forward_kinematics(joint, up_to_joint=i)
            z_i = T[0:3, 2]
            p_i = T[0:3, 3]
            z_axes.append(z_i)
            p_positions.append(p_i)

        # End effector position pe is the origin of frame 5
        pe = p_positions[-1]

        # Build Jacobian 6x5
        jacobian = np.zeros((6, 5))
        for i in range(5):
            zi = z_axes[i]
            pi = p_positions[i]
            # revolute joint Jacobian
            jacobian[0:3, i] = np.cross(zi, pe - pi)   # linear velocity part
            jacobian[3:6, i] = zi                      # angular velocity part

        # Use a threshold value and treat any element with a small absolute value as 0
        threshold = 1e-6
        jacobian[np.abs(jacobian) < threshold] = 0.0

        # Your code ends here ------------------------------
        # ╔════════════════════════════════════════════════════════════════════════╗
        # ╚════════════════════════════════════════════════════════════════════════╝
        assert jacobian.shape == (6, 5)
        return jacobian

def main(args=None):
    rclpy.init(args=args)
    node = YoubotKinematicModel()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
