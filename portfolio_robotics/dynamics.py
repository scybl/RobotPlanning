"""ROS-free IIWA14 dynamics routines for quick numerical checks."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import pi
from typing import Sequence

import numpy as np


@dataclass
class Iiwa14Dynamics:
    """Manual IIWA14 kinematics and dynamics model used by the quick demo."""

    gravity: float = 9.8
    x_alpha: np.ndarray = field(
        default_factory=lambda: np.array([pi / 2, pi / 2, pi / 2, pi / 2, pi / 2, pi / 2, 0.0])
    )
    y_alpha: np.ndarray = field(default_factory=lambda: np.array([pi, pi, 0.0, pi, 0.0, pi, 0.0]))
    translation_vec: np.ndarray = field(
        default_factory=lambda: np.array(
            [
                [0.0, 0.0, 0.2025],
                [0.0, 0.2045, 0.0],
                [0.0, 0.0, 0.2155],
                [0.0, 0.1845, 0.0],
                [0.0, 0.0, 0.2155],
                [0.0, 0.081, 0.0],
                [0.0, 0.0, 0.045],
            ],
            dtype=float,
        )
    )
    link_cm: np.ndarray = field(
        default_factory=lambda: np.array(
            [
                [0.0, -0.03, 0.12],
                [0.0003, 0.059, 0.042],
                [0.0, 0.03, 0.13],
                [0.0, 0.067, 0.034],
                [0.0001, 0.021, 0.076],
                [0.0, 0.0006, 0.0004],
                [0.0, 0.0, 0.02],
            ],
            dtype=float,
        )
    )
    mass: np.ndarray = field(default_factory=lambda: np.array([4.0, 4.0, 3.0, 2.7, 1.7, 1.8, 0.3]))
    ixyz: np.ndarray = field(
        default_factory=lambda: np.array(
            [
                [0.1, 0.09, 0.02],
                [0.05, 0.018, 0.044],
                [0.08, 0.075, 0.01],
                [0.03, 0.01, 0.029],
                [0.02, 0.018, 0.005],
                [0.005, 0.0036, 0.0047],
                [0.001, 0.001, 0.001],
            ],
            dtype=float,
        )
    )

    @property
    def n_joints(self) -> int:
        return 7

    @staticmethod
    def translation(vector: Sequence[float]) -> np.ndarray:
        transform = np.eye(4)
        transform[:3, 3] = np.asarray(vector, dtype=float)
        return transform

    @staticmethod
    def rotation_x(theta: float) -> np.ndarray:
        c = np.cos(theta)
        s = np.sin(theta)
        transform = np.eye(4)
        transform[1, 1] = c
        transform[1, 2] = -s
        transform[2, 1] = s
        transform[2, 2] = c
        return transform

    @staticmethod
    def rotation_y(theta: float) -> np.ndarray:
        c = np.cos(theta)
        s = np.sin(theta)
        transform = np.eye(4)
        transform[0, 0] = c
        transform[0, 2] = s
        transform[2, 0] = -s
        transform[2, 2] = c
        return transform

    @staticmethod
    def rotation_z(theta: float) -> np.ndarray:
        c = np.cos(theta)
        s = np.sin(theta)
        transform = np.eye(4)
        transform[0, 0] = c
        transform[0, 1] = -s
        transform[1, 0] = s
        transform[1, 1] = c
        return transform

    def forward_kinematics(self, joint_readings: Sequence[float], up_to_joint: int = 7) -> np.ndarray:
        q = self._joint_array(joint_readings)
        if not 0 <= up_to_joint <= self.n_joints:
            raise ValueError("up_to_joint must be between 0 and 7.")

        transform = np.eye(4)
        transform[2, 3] = 0.1575
        for idx in range(up_to_joint):
            transform = transform @ self.rotation_z(q[idx])
            transform = transform @ self.translation(self.translation_vec[idx])
            transform = transform @ self.rotation_x(self.x_alpha[idx])
            transform = transform @ self.rotation_y(self.y_alpha[idx])
        return transform

    def forward_kinematics_centre_of_mass(
        self,
        joint_readings: Sequence[float],
        up_to_joint: int = 7,
    ) -> np.ndarray:
        if not 1 <= up_to_joint <= self.n_joints:
            raise ValueError("up_to_joint must be between 1 and 7 for a centre of mass.")
        q = self._joint_array(joint_readings)
        transform = self.forward_kinematics(q, up_to_joint - 1)
        transform = transform @ self.rotation_z(q[up_to_joint - 1])
        transform = transform @ self.translation(self.link_cm[up_to_joint - 1])
        return transform

    def jacobian_centre_of_mass(
        self,
        joint_readings: Sequence[float],
        up_to_joint: int = 7,
    ) -> np.ndarray:
        q = self._joint_array(joint_readings)
        com_position = self.forward_kinematics_centre_of_mass(q, up_to_joint)[:3, 3]
        jacobian = np.zeros((6, self.n_joints))

        transform = np.eye(4)
        transform[2, 3] = 0.1575
        for idx in range(up_to_joint):
            z_axis = transform[:3, 2]
            joint_position = transform[:3, 3]
            jacobian[:3, idx] = np.cross(z_axis, com_position - joint_position)
            jacobian[3:, idx] = z_axis

            transform = transform @ self.rotation_z(q[idx])
            transform = transform @ self.translation(self.translation_vec[idx])
            transform = transform @ self.rotation_x(self.x_alpha[idx])
            transform = transform @ self.rotation_y(self.y_alpha[idx])
        return jacobian

    def inertia_matrix(self, joint_readings: Sequence[float]) -> np.ndarray:
        q = self._joint_array(joint_readings)
        inertia = np.zeros((self.n_joints, self.n_joints))

        for idx in range(self.n_joints):
            jacobian = self.jacobian_centre_of_mass(q, up_to_joint=idx + 1)
            jv = np.zeros((3, self.n_joints))
            jw = np.zeros((3, self.n_joints))
            jv[:, : idx + 1] = jacobian[:3, : idx + 1]
            jw[:, : idx + 1] = jacobian[3:, : idx + 1]

            rotation = self.forward_kinematics(q, up_to_joint=idx + 1)[:3, :3]
            body_inertia = np.diag(self.ixyz[idx])
            world_inertia = rotation @ body_inertia @ rotation.T
            inertia += self.mass[idx] * (jv.T @ jv) + jw.T @ world_inertia @ jw

        return 0.5 * (inertia + inertia.T)

    def coriolis_times_qdot(
        self,
        joint_readings: Sequence[float],
        joint_velocities: Sequence[float],
        eps: float = 1e-6,
    ) -> np.ndarray:
        q = self._joint_array(joint_readings)
        qd = self._joint_array(joint_velocities)
        n = self.n_joints
        d_b = np.zeros((n, n, n))

        for axis in range(n):
            q_plus = q.copy()
            q_minus = q.copy()
            q_plus[axis] += eps
            q_minus[axis] -= eps
            d_b[:, :, axis] = (self.inertia_matrix(q_plus) - self.inertia_matrix(q_minus)) / (2.0 * eps)

        coriolis = np.zeros(n)
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    christoffel = 0.5 * (d_b[i, j, k] + d_b[i, k, j] - d_b[j, k, i])
                    coriolis[i] += christoffel * qd[j] * qd[k]
        return coriolis

    def gravity_vector(self, joint_readings: Sequence[float]) -> np.ndarray:
        q = self._joint_array(joint_readings)
        gravity_force = np.array([0.0, 0.0, -self.gravity])
        gravity = np.zeros(self.n_joints)

        for idx in range(self.n_joints):
            jacobian = self.jacobian_centre_of_mass(q, up_to_joint=idx + 1)
            jv = np.zeros((3, self.n_joints))
            jv[:, : idx + 1] = jacobian[:3, : idx + 1]
            gravity -= jv.T @ (self.mass[idx] * gravity_force)
        return gravity

    def joint_acceleration(
        self,
        joint_readings: Sequence[float],
        joint_velocities: Sequence[float],
        torque: Sequence[float] | None = None,
    ) -> np.ndarray:
        q = self._joint_array(joint_readings)
        qd = self._joint_array(joint_velocities)
        tau = np.zeros(self.n_joints) if torque is None else self._joint_array(torque)
        return np.linalg.solve(
            self.inertia_matrix(q),
            tau - self.coriolis_times_qdot(q, qd) - self.gravity_vector(q),
        )

    def _joint_array(self, values: Sequence[float]) -> np.ndarray:
        array = np.asarray(values, dtype=float)
        if array.shape != (self.n_joints,):
            raise ValueError("Expected seven joint values.")
        return array
