"""Lightweight kinematics utilities extracted from the ROS stack."""

from __future__ import annotations

import math
from typing import Mapping, Sequence

import numpy as np

DHTable = Mapping[str, Sequence[float]]

YOUBOT_URDF_DH = {
    "a": [0.033, 0.155, 0.135, 0.0, -0.002],
    "alpha": [math.pi / 2, 0.0, 0.0, -math.pi / 2, 0.0],
    "d": [0.147, 0.019, 0.0, 0.0, 0.185],
    "theta": [0.0, math.pi / 2, 0.0, -math.pi / 2, 0.0],
}

YOUBOT_JOINT_OFFSETS = np.deg2rad([170.0, 65.0, -146.0, 102.5, 167.5])
YOUBOT_JOINT_POLARITY = np.array([-1.0, 1.0, 1.0, 1.0, 1.0])


def _normalised_quaternion_wxyz(q_wxyz: Sequence[float]) -> np.ndarray:
    q = np.asarray(q_wxyz, dtype=float)
    if q.shape != (4,):
        raise ValueError("Quaternion must be [w, x, y, z].")
    norm = np.linalg.norm(q)
    if norm == 0.0:
        raise ValueError("Zero-length quaternion cannot be normalised.")
    return q / norm


def quaternion_to_euler_zyx(q_wxyz: Sequence[float]) -> np.ndarray:
    """Convert quaternion [w, x, y, z] to roll, pitch, yaw for ZYX Euler angles."""
    w, x, y, z = _normalised_quaternion_wxyz(q_wxyz)
    roll = math.atan2(2.0 * (w * x + y * z), 1.0 - 2.0 * (x * x + y * y))
    pitch_arg = 2.0 * (w * y - z * x)
    pitch = math.asin(float(np.clip(pitch_arg, -1.0, 1.0)))
    yaw = math.atan2(2.0 * (w * z + x * y), 1.0 - 2.0 * (y * y + z * z))
    return np.array([roll, pitch, yaw], dtype=float)


def quaternion_to_rodrigues(q_wxyz: Sequence[float]) -> np.ndarray:
    """Convert quaternion [w, x, y, z] to a Rodrigues vector."""
    w, x, y, z = _normalised_quaternion_wxyz(q_wxyz)
    vector = np.array([x, y, z], dtype=float)
    if np.linalg.norm(vector) < 1e-12:
        return np.zeros(3)
    if abs(w) < 1e-12:
        return np.sign(w if w else 1.0) * np.full(3, np.inf)
    return vector / w


def standard_dh(a: float, alpha: float, d: float, theta: float) -> np.ndarray:
    """Return the standard Denavit-Hartenberg transform."""
    ct = math.cos(theta)
    st = math.sin(theta)
    ca = math.cos(alpha)
    sa = math.sin(alpha)
    return np.array(
        [
            [ct, -st * ca, st * sa, a * ct],
            [st, ct * ca, -ct * sa, a * st],
            [0.0, sa, ca, d],
            [0.0, 0.0, 0.0, 1.0],
        ],
        dtype=float,
    )


def forward_kinematics(
    dh_table: DHTable,
    joint_readings: Sequence[float],
    up_to_joint: int | None = None,
) -> np.ndarray:
    """Multiply DH transforms from the base to ``up_to_joint``."""
    joint_values = np.asarray(joint_readings, dtype=float)
    n_joints = len(dh_table["a"])
    if up_to_joint is None:
        up_to_joint = n_joints
    if not 0 <= up_to_joint <= n_joints:
        raise ValueError("up_to_joint is outside the DH table range.")
    if joint_values.shape[0] < up_to_joint:
        raise ValueError("Not enough joint readings supplied.")

    transform = np.eye(4)
    for idx in range(up_to_joint):
        transform = transform @ standard_dh(
            float(dh_table["a"][idx]),
            float(dh_table["alpha"][idx]),
            float(dh_table["d"][idx]),
            float(dh_table["theta"][idx]) + float(joint_values[idx]),
        )
    return transform


def _offset_youbot_dh() -> dict[str, list[float]]:
    table = {key: list(values) for key, values in YOUBOT_URDF_DH.items()}
    table["theta"] = [
        theta + offset for theta, offset in zip(table["theta"], YOUBOT_JOINT_OFFSETS)
    ]
    return table


def youbot_forward_kinematics(
    joint_readings: Sequence[float],
    up_to_joint: int = 5,
    apply_offsets: bool = True,
) -> np.ndarray:
    """Forward kinematics for the YouBot arm model used in the ROS stack."""
    joint_values = np.asarray(joint_readings, dtype=float)
    if joint_values.shape != (5,):
        raise ValueError("YouBot joint_readings must contain five values.")
    dh_table = _offset_youbot_dh() if apply_offsets else YOUBOT_URDF_DH
    corrected = YOUBOT_JOINT_POLARITY * joint_values if apply_offsets else joint_values
    return forward_kinematics(dh_table, corrected, up_to_joint)


def youbot_jacobian(joint_readings: Sequence[float]) -> np.ndarray:
    """Analytical 6x5 YouBot Jacobian using the same base axis convention as KDL."""
    joint_values = np.asarray(joint_readings, dtype=float)
    if joint_values.shape != (5,):
        raise ValueError("YouBot joint_readings must contain five values.")

    z_axes = [np.array([0.0, 0.0, -1.0])]
    positions = [np.zeros(3)]
    for idx in range(1, 6):
        transform = youbot_forward_kinematics(joint_values, up_to_joint=idx)
        z_axes.append(transform[:3, 2])
        positions.append(transform[:3, 3])

    end_effector = positions[-1]
    jacobian = np.zeros((6, 5))
    for idx in range(5):
        jacobian[:3, idx] = np.cross(z_axes[idx], end_effector - positions[idx])
        jacobian[3:, idx] = z_axes[idx]

    jacobian[np.abs(jacobian) < 1e-9] = 0.0
    return jacobian
