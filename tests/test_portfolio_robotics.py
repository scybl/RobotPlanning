"""Numerical correctness tests for the ROS-free algorithm layer."""

from __future__ import annotations

import math

import numpy as np

from portfolio_robotics.dynamics import Iiwa14Dynamics
from portfolio_robotics.kinematics import (
    forward_kinematics,
    quaternion_to_euler_zyx,
    quaternion_to_rodrigues,
    youbot_forward_kinematics,
    youbot_jacobian,
)
from portfolio_robotics.planning import (
    interpolate_transform,
    make_transform,
    path_length,
    shortest_path_order,
)


def _rotation_z(angle: float) -> np.ndarray:
    cosine = math.cos(angle)
    sine = math.sin(angle)
    return np.array(
        [[cosine, -sine, 0.0], [sine, cosine, 0.0], [0.0, 0.0, 1.0]]
    )


def test_quaternion_conversions_for_known_y_rotation():
    angle = math.pi / 4.0
    quaternion = [math.cos(angle / 2.0), 0.0, math.sin(angle / 2.0), 0.0]

    np.testing.assert_allclose(
        quaternion_to_euler_zyx(quaternion), [0.0, angle, 0.0], atol=1e-12
    )
    np.testing.assert_allclose(
        quaternion_to_rodrigues(quaternion), [0.0, math.tan(angle / 2.0), 0.0], atol=1e-12
    )


def test_forward_kinematics_matches_two_link_planar_geometry():
    dh_table = {
        "a": [1.0, 1.0],
        "alpha": [0.0, 0.0],
        "d": [0.0, 0.0],
        "theta": [0.0, 0.0],
    }

    transform = forward_kinematics(dh_table, [math.pi / 2.0, -math.pi / 2.0])

    np.testing.assert_allclose(transform[:3, 3], [1.0, 1.0, 0.0], atol=1e-12)
    np.testing.assert_allclose(transform[:3, :3], np.eye(3), atol=1e-12)


def test_youbot_zero_configuration_without_offsets_has_known_pose():
    transform = youbot_forward_kinematics(np.zeros(5), apply_offsets=False)

    np.testing.assert_allclose(transform[:3, 3], [0.031, -0.019, 0.622], atol=1e-12)
    np.testing.assert_allclose(transform[:3, :3], np.eye(3), atol=1e-12)
    np.testing.assert_allclose(transform[3], [0.0, 0.0, 0.0, 1.0], atol=0.0)


def test_youbot_jacobian_linear_part_matches_fk_finite_difference():
    joints = np.array([0.15, -0.35, 0.25, -0.20, 0.10])
    jacobian = youbot_jacobian(joints)
    epsilon = 1e-7
    numerical_linear = np.zeros((3, 5))

    for joint_index in range(5):
        perturbation = np.zeros(5)
        perturbation[joint_index] = epsilon
        position_plus = youbot_forward_kinematics(joints + perturbation)[:3, 3]
        position_minus = youbot_forward_kinematics(joints - perturbation)[:3, 3]
        numerical_linear[:, joint_index] = (position_plus - position_minus) / (2.0 * epsilon)

    assert jacobian.shape == (6, 5)
    assert np.linalg.matrix_rank(jacobian) == 5
    np.testing.assert_allclose(jacobian[:3], numerical_linear, atol=2e-8)


def test_path_length_matches_known_right_angle_polyline():
    points = np.array([[3.0, 0.0, 0.0], [3.0, 4.0, 0.0], [0.0, 4.0, 0.0]])

    assert path_length(points) == 10.0


def test_shortest_path_order_finds_unique_minimum():
    checkpoints = np.array([[3.0, 0.0, 0.0], [1.0, 0.0, 0.0], [2.0, 1.0, 0.0]])

    order, distance = shortest_path_order(checkpoints)

    assert order == [1, 2, 0]
    assert math.isclose(distance, 1.0 + 2.0 * math.sqrt(2.0), abs_tol=1e-12)
    assert math.isclose(distance, path_length(checkpoints[order]), abs_tol=1e-12)


def test_interpolate_transform_has_correct_midpoint_pose():
    start = make_transform([0.0, 0.0, 0.0], _rotation_z(0.0))
    end = make_transform([2.0, 4.0, 6.0], _rotation_z(math.pi))

    poses = interpolate_transform(start, end, num_points=3)

    np.testing.assert_allclose(poses[0], start, atol=1e-12)
    np.testing.assert_allclose(poses[-1], end, atol=1e-12)
    np.testing.assert_allclose(poses[1, :3, 3], [1.0, 2.0, 3.0], atol=1e-12)
    np.testing.assert_allclose(poses[1, :3, :3], _rotation_z(math.pi / 2.0), atol=1e-12)


def test_iiwa_zero_configuration_has_known_straight_up_pose():
    model = Iiwa14Dynamics()

    transform = model.forward_kinematics(np.zeros(7))

    np.testing.assert_allclose(transform[:3, 3], [0.0, 0.0, 1.306], atol=1e-12)
    np.testing.assert_allclose(transform[:3, :3], np.eye(3), atol=1e-12)


def test_iiwa_inertia_matrix_is_symmetric_positive_definite():
    model = Iiwa14Dynamics()
    joints = np.array([0.0, 0.1, -0.2, 0.3, -0.4, 0.5, -0.1])

    inertia = model.inertia_matrix(joints)

    assert inertia.shape == (7, 7)
    np.testing.assert_allclose(inertia, inertia.T, atol=1e-12)
    assert np.linalg.eigvalsh(inertia).min() > 0.0


def test_iiwa_gravity_compensation_produces_zero_acceleration_at_rest():
    model = Iiwa14Dynamics()
    joints = np.array([0.0, 0.1, -0.2, 0.3, -0.4, 0.5, -0.1])
    velocities = np.zeros(7)
    gravity_compensation = model.gravity_vector(joints)

    acceleration = model.joint_acceleration(joints, velocities, gravity_compensation)

    np.testing.assert_allclose(acceleration, np.zeros(7), atol=1e-12)
