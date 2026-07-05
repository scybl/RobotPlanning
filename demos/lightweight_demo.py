#!/usr/bin/env python3
"""Run deterministic numerical checks without a ROS installation."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from portfolio_robotics import (
    Iiwa14Dynamics,
    interpolate_transform,
    path_length,
    quaternion_to_euler_zyx,
    quaternion_to_rodrigues,
    shortest_path_order,
    youbot_forward_kinematics,
    youbot_jacobian,
)
from portfolio_robotics.planning import make_transform


def _fmt_vector(values: np.ndarray, precision: int = 4) -> str:
    return "[" + ", ".join(f"{value:+.{precision}f}" for value in values) + "]"


def quaternion_demo() -> None:
    quat_wxyz = np.array([0.92387953, 0.0, 0.38268343, 0.0])
    roll, pitch, yaw = quaternion_to_euler_zyx(quat_wxyz)
    rodrigues = quaternion_to_rodrigues(quat_wxyz)

    print("Quaternion demo")
    print(f"  Euler ZYX [rad]      roll={roll:+.4f} pitch={pitch:+.4f} yaw={yaw:+.4f}")
    print(f"  Rodrigues vector     {_fmt_vector(rodrigues)}")


def youbot_demo() -> None:
    joints = np.array([0.15, -0.35, 0.25, -0.20, 0.10])
    pose = youbot_forward_kinematics(joints)
    jacobian = youbot_jacobian(joints)

    print("\nYouBot kinematics demo")
    print(f"  Joint sample [rad]   {_fmt_vector(joints)}")
    print(f"  End-effector xyz [m] {_fmt_vector(pose[:3, 3])}")
    print(f"  Jacobian shape/rank  {jacobian.shape} / {np.linalg.matrix_rank(jacobian)}")
    print(f"  Jacobian Frobenius   {np.linalg.norm(jacobian):.4f}")


def planning_demo() -> None:
    checkpoint_positions = np.array(
        [
            [0.34, 0.08, 0.28],
            [0.18, -0.16, 0.36],
            [0.41, -0.05, 0.23],
            [0.23, 0.18, 0.31],
        ]
    )
    start = np.array([0.12, 0.0, 0.25])
    order, best_length = shortest_path_order(checkpoint_positions, start)
    ordered_points = checkpoint_positions[order]

    interpolated = interpolate_transform(
        make_transform(ordered_points[0]),
        make_transform(ordered_points[1]),
        num_points=6,
    )

    print("\nCheckpoint planning demo")
    print(f"  Shortest order       {order}")
    print(f"  Ordered path length  {best_length:.4f} m")
    print(f"  Recomputed length    {path_length(ordered_points, start):.4f} m")
    print(f"  First interpolation  {_fmt_vector(interpolated[1, :3, 3])}")


def iiwa_demo() -> None:
    model = Iiwa14Dynamics()
    q = np.array([0.0, 0.1, -0.2, 0.3, -0.4, 0.5, -0.1])
    qd = np.array([0.0, 0.05, 0.03, -0.02, 0.01, -0.04, 0.02])

    pose = model.forward_kinematics(q)
    inertia = model.inertia_matrix(q)
    gravity = model.gravity_vector(q)
    acceleration = model.joint_acceleration(q, qd)
    symmetry_error = np.linalg.norm(inertia - inertia.T)
    min_eigenvalue = float(np.linalg.eigvalsh(inertia).min())

    print("\nIIWA dynamics demo")
    print(f"  End-effector xyz [m] {_fmt_vector(pose[:3, 3])}")
    print(f"  Inertia symmetry err {symmetry_error:.2e}")
    print(f"  Min inertia eig      {min_eigenvalue:.4f}")
    print(f"  Gravity norm         {np.linalg.norm(gravity):.4f}")
    print(f"  Passive qdd sample   {_fmt_vector(acceleration, precision=3)}")


def main() -> None:
    quaternion_demo()
    youbot_demo()
    planning_demo()
    iiwa_demo()


if __name__ == "__main__":
    main()
