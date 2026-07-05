#!/usr/bin/env python3

import numpy as np
import PyKDL
from ament_index_python.packages import get_package_share_directory
from iiwa_dynamics.iiwa14DynBase import Iiwa14DynamicBase
from iiwa_dynamics.urdf_kdl_utils import build_kdl_chain_from_urdf

class Iiwa14DynamicModel(Iiwa14DynamicBase):
    def __init__(self):
        super(Iiwa14DynamicModel, self).__init__(tf_suffix='model')
        urdf_path = get_package_share_directory('iiwa_dynamics') + '/model.urdf'
        with open(urdf_path, 'r', encoding='utf-8') as f:
            robot_description = f.read()
        self.kine_chain = build_kdl_chain_from_urdf(robot_description, "iiwa_link_0", "iiwa_link_ee")
        self.NJoints = self.kine_chain.getNrOfJoints()
        self.jac_calc = PyKDL.ChainJntToJacSolver(self.kine_chain)
        self.dyn_solver = PyKDL.ChainDynParam(self.kine_chain, PyKDL.Vector(0, 0, -self.g))


    def forward_kinematics(self, joints_readings, up_to_joint=7):
        """Compute forward kinematics up to the selected joint."""
        assert isinstance(joints_readings, list), "joint readings of type " + str(type(joints_readings))
        assert isinstance(up_to_joint, int)
        ############################################################################
        ############################################################################
        T = np.identity(4)
        T[2, 3] = 0.1575

        # R_z->T->R_x->R_y
        for i in range(up_to_joint):
            T = T.dot(self.T_rotationZ(joints_readings[i]))
            T = T.dot(self.T_translation(self.translation_vec[i]))
            T = T.dot(self.T_rotationX(self.X_alpha[i]))
            T = T.dot(self.T_rotationY(self.Y_alpha[i]))
            
        return T
        ############################################################################
        ############################################################################


    def get_jacobian_centre_of_mass(self, joint_readings, up_to_joint=7):
    ############################################################################
    ############################################################################
        NJ = self.NJoints
        J = np.zeros((6, NJ))

        # get the Homogeneous
        T_com = self.forward_kinematics_centre_of_mass(joint_readings, up_to_joint)
        p_com = T_com[0:3, 3]

        # calculate the ans
        T = np.identity(4)
        T[2, 3] = 0.1575   # base offset

        p_i = T[0:3, 3]  
        for i in range(up_to_joint):

            z_i = T[0:3, 2]

            # linear velocity
            Jv_i = np.cross(z_i, (p_com - p_i))
            J[0:3, i] = Jv_i

            # angular velocity
            J[3:6, i] = z_i

            if i < up_to_joint:
                T = T.dot(self.T_rotationZ(joint_readings[i]))
                T = T.dot(self.T_translation(self.translation_vec[i]))
                T = T.dot(self.T_rotationX(self.X_alpha[i]))
                T = T.dot(self.T_rotationY(self.Y_alpha[i]))

                p_i = T[0:3, 3]

        return J
        ############################################################################
        ############################################################################

    def forward_kinematics_centre_of_mass(self, joints_readings, up_to_joint=7):
        """This function computes the forward kinematics up to the centre of mass for the given joint frame.
        Reference - Lecture 9 slide 14.
        Args:
            joints_readings (list): the state of the robot joints.
            up_to_joint (int, optional): Specify up to what frame you want to compute forward kinematicks.
                Defaults to 5.
        Returns:
            np.ndarray: A 4x4 homogeneous transformation matrix describing the pose of frame_{up_to_joint} for the
            centre of mass w.r.t the base of the robot.
        """
        
        T= np.identity(4)
        T[2, 3] = 0.1575

        T = self.forward_kinematics(joints_readings, up_to_joint-1)
        T = T.dot(self.T_rotationZ(joints_readings[up_to_joint-1]))
        T = T.dot(self.T_translation(self.link_cm[up_to_joint-1, :]))

        return T


    def get_B(self, joint_readings):
        """Given the joint positions of the robot, compute inertia matrix B.
        Args:
            joint_readings (list): The positions of the robot joints.

        Returns:
            B (numpy.ndarray): The output is a numpy 7*7 matrix describing the inertia matrix B.
        """
        assert isinstance(joint_readings, list)
        assert len(joint_readings) == self.NJoints
        ############################################################################
        ############################################################################
        B = np.zeros((self.NJoints, self.NJoints))

        for i in range(self.NJoints):
            # i+1th CoM Jacobian ----
            Jci = self.get_jacobian_centre_of_mass(
                joint_readings,
                up_to_joint=i + 1
            )
            Jv = Jci[0:3, :]   # 3×7
            Jw = Jci[3:6, :]   # 3×7

            Jv_full = np.zeros((3, self.NJoints))
            Jw_full = np.zeros((3, self.NJoints))
            Jv_full[:, :i+1] = Jv[:, :i+1]
            Jw_full[:, :i+1] = Jw[:, :i+1]

            # link position matrix R_i (base <- link_i) ----
            Ti = self.forward_kinematics(joint_readings, up_to_joint=i + 1)
            Ri = Ti[0:3, 0:3]

            I_body = np.diag(self.Ixyz[i, :])

            # to world frame
            I_world = Ri @ I_body @ Ri.T

            mi = self.mass[i]
            B_link = mi * (Jv_full.T @ Jv_full) + (Jw_full.T @ I_world @ Jw_full)

            B += B_link

        B = 0.5 * (B + B.T)


        return B
        ############################################################################
        ############################################################################


    def get_C_times_qdot(self, joint_readings, joint_velocities):
        """Given the joint positions and velocities of the robot, compute Coriolis terms C.
        Args:
            joint_readings (list): The positions of the robot joints.
            joint_velocities (list): The velocities of the robot joints.

        Returns:
            C (numpy.ndarray): The output is a numpy 7*1 matrix describing the Coriolis terms C times joint velocities.
        """
        assert isinstance(joint_readings, list)
        assert len(joint_readings) == 7
        assert isinstance(joint_velocities, list)
        assert len(joint_velocities) == 7
        ############################################################################
        ############################################################################
        q = np.array(joint_readings)
        qd = np.array(joint_velocities)
        n = self.NJoints
        dB = np.zeros((n, n, n))
        Cq = np.zeros(n)
        eps = 1e-6

        for axis in range(n):
            dq = np.zeros(n)
            dq[axis] = eps
            B_plus = self.get_B(list(q + dq))
            B_minus = self.get_B(list(q - dq))
            dB[:, :, axis] = (B_plus - B_minus) / (2.0 * eps)

        for i in range(n):
            for j in range(n):
                for k in range(n):
                    dBij_dqk = dB[i, j, k]
                    dBik_dqj = dB[i, k, j]
                    dBjk_dqi = dB[j, k, i]
                    cijk = 0.5 * (dBij_dqk + dBik_dqj - dBjk_dqi)
                    Cq[i] += cijk * qd[j] * qd[k]

        return Cq
        ############################################################################
        ############################################################################

    def get_G(self, joint_readings):
        """Given the joint positions of the robot, compute the gravity matrix g."""

        assert isinstance(joint_readings, list)
        assert len(joint_readings) == 7
        ############################################################################
        ############################################################################
        g_vec = np.array([0.0, 0.0, -self.g])   # gravity points in -Z
        G = np.zeros(self.NJoints)

        for i in range(1, 8):   # link 1 → link 7

            # mass of link i
            mi = self.mass[i-1]

            # Jacobian at COM of link i (shape 6×7)
            Jci = self.get_jacobian_centre_of_mass(
                joint_readings,
                up_to_joint=i
            )

            # take only linear part (3×7)
            Jv = Jci[0:3, :]

            # build truncated Jacobian so only first i joints affect link i
            Jv_full = np.zeros((3, self.NJoints))
            Jv_full[:, :i] = Jv[:, :i]

            # gravity force on this link
            Fg = mi * g_vec

            # NOTE: minus sign to match validation reference
            G -= Jv_full.T @ Fg

        return G
        ############################################################################
        ############################################################################
