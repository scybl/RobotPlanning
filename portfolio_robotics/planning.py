"""Small planning utilities for the portfolio demo."""

from __future__ import annotations

import itertools
from typing import Sequence

import numpy as np


def shortest_path_order(
    checkpoint_positions: Sequence[Sequence[float]],
    start_position: Sequence[float] | None = None,
) -> tuple[list[int], float]:
    """Return the checkpoint order with the shortest Cartesian path length."""
    positions = np.asarray(checkpoint_positions, dtype=float)
    if positions.ndim != 2 or positions.shape[1] != 3:
        raise ValueError("checkpoint_positions must have shape (N, 3).")
    if len(positions) == 0:
        return [], 0.0
    start = np.zeros(3) if start_position is None else np.asarray(start_position, dtype=float)

    best_order: tuple[int, ...] | None = None
    best_distance = float("inf")
    for order in itertools.permutations(range(len(positions))):
        distance = float(np.linalg.norm(positions[order[0]] - start))
        for left, right in zip(order[:-1], order[1:]):
            distance += float(np.linalg.norm(positions[right] - positions[left]))
        if distance < best_distance:
            best_order = order
            best_distance = distance

    return list(best_order or ()), best_distance


def path_length(points: Sequence[Sequence[float]], start_position: Sequence[float] | None = None) -> float:
    """Compute the Cartesian path length through ordered points."""
    positions = np.asarray(points, dtype=float)
    if len(positions) == 0:
        return 0.0
    start = np.zeros(3) if start_position is None else np.asarray(start_position, dtype=float)
    length = float(np.linalg.norm(positions[0] - start))
    for left, right in zip(positions[:-1], positions[1:]):
        length += float(np.linalg.norm(right - left))
    return length


def make_transform(position: Sequence[float], rotation: np.ndarray | None = None) -> np.ndarray:
    """Create a homogeneous transform from a translation and optional 3x3 rotation."""
    transform = np.eye(4)
    transform[:3, 3] = np.asarray(position, dtype=float)
    if rotation is not None:
        transform[:3, :3] = np.asarray(rotation, dtype=float)
    return transform


def rot_to_quat_xyzw(rotation: np.ndarray) -> np.ndarray:
    """Convert a 3x3 rotation matrix to quaternion [x, y, z, w]."""
    matrix = np.asarray(rotation, dtype=float)
    trace = float(np.trace(matrix))
    if trace > 0.0:
        scale = np.sqrt(trace + 1.0) * 2.0
        qw = 0.25 * scale
        qx = (matrix[2, 1] - matrix[1, 2]) / scale
        qy = (matrix[0, 2] - matrix[2, 0]) / scale
        qz = (matrix[1, 0] - matrix[0, 1]) / scale
    else:
        axis = int(np.argmax(np.diag(matrix)))
        if axis == 0:
            scale = np.sqrt(1.0 + matrix[0, 0] - matrix[1, 1] - matrix[2, 2]) * 2.0
            qw = (matrix[2, 1] - matrix[1, 2]) / scale
            qx = 0.25 * scale
            qy = (matrix[0, 1] + matrix[1, 0]) / scale
            qz = (matrix[0, 2] + matrix[2, 0]) / scale
        elif axis == 1:
            scale = np.sqrt(1.0 + matrix[1, 1] - matrix[0, 0] - matrix[2, 2]) * 2.0
            qw = (matrix[0, 2] - matrix[2, 0]) / scale
            qx = (matrix[0, 1] + matrix[1, 0]) / scale
            qy = 0.25 * scale
            qz = (matrix[1, 2] + matrix[2, 1]) / scale
        else:
            scale = np.sqrt(1.0 + matrix[2, 2] - matrix[0, 0] - matrix[1, 1]) * 2.0
            qw = (matrix[1, 0] - matrix[0, 1]) / scale
            qx = (matrix[0, 2] + matrix[2, 0]) / scale
            qy = (matrix[1, 2] + matrix[2, 1]) / scale
            qz = 0.25 * scale
    quat = np.array([qx, qy, qz, qw], dtype=float)
    return quat / np.linalg.norm(quat)


def quat_xyzw_to_rot(quat_xyzw: Sequence[float]) -> np.ndarray:
    """Convert quaternion [x, y, z, w] to a 3x3 rotation matrix."""
    qx, qy, qz, qw = np.asarray(quat_xyzw, dtype=float)
    norm = np.linalg.norm([qx, qy, qz, qw])
    if norm == 0.0:
        return np.eye(3)
    qx, qy, qz, qw = np.array([qx, qy, qz, qw], dtype=float) / norm
    return np.array(
        [
            [1.0 - 2.0 * (qy * qy + qz * qz), 2.0 * (qx * qy - qw * qz), 2.0 * (qx * qz + qw * qy)],
            [2.0 * (qx * qy + qw * qz), 1.0 - 2.0 * (qx * qx + qz * qz), 2.0 * (qy * qz - qw * qx)],
            [2.0 * (qx * qz - qw * qy), 2.0 * (qy * qz + qw * qx), 1.0 - 2.0 * (qx * qx + qy * qy)],
        ],
        dtype=float,
    )


def slerp(quat_a: Sequence[float], quat_b: Sequence[float], t: float) -> np.ndarray:
    """Spherical linear interpolation for quaternions [x, y, z, w]."""
    qa = np.asarray(quat_a, dtype=float)
    qb = np.asarray(quat_b, dtype=float)
    qa = qa / np.linalg.norm(qa)
    qb = qb / np.linalg.norm(qb)

    dot = float(np.dot(qa, qb))
    if dot < 0.0:
        qb = -qb
        dot = -dot
    if dot > 0.9995:
        result = qa + t * (qb - qa)
        return result / np.linalg.norm(result)

    theta_0 = np.arccos(dot)
    theta = theta_0 * t
    sin_theta_0 = np.sin(theta_0)
    return (
        np.sin(theta_0 - theta) / sin_theta_0 * qa
        + np.sin(theta) / sin_theta_0 * qb
    )


def interpolate_transform(transform_a: np.ndarray, transform_b: np.ndarray, num_points: int) -> np.ndarray:
    """Interpolate translation linearly and rotation with SLERP."""
    if num_points < 1:
        raise ValueError("num_points must be at least 1.")
    ta = np.asarray(transform_a, dtype=float)
    tb = np.asarray(transform_b, dtype=float)
    qa = rot_to_quat_xyzw(ta[:3, :3])
    qb = rot_to_quat_xyzw(tb[:3, :3])
    output = np.zeros((num_points, 4, 4))

    for idx in range(num_points):
        fraction = 1.0 if num_points == 1 else idx / (num_points - 1)
        transform = np.eye(4)
        transform[:3, 3] = (1.0 - fraction) * ta[:3, 3] + fraction * tb[:3, 3]
        transform[:3, :3] = quat_xyzw_to_rot(slerp(qa, qb, fraction))
        output[idx] = transform
    return output
