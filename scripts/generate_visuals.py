#!/usr/bin/env python3
"""Generate reproducible plots from the ROS-free robotics algorithms."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import matplotlib
import numpy as np

matplotlib.use("Agg")
from matplotlib import pyplot as plt  # noqa: E402


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from portfolio_robotics import (  # noqa: E402
    interpolate_transform,
    path_length,
    shortest_path_order,
    youbot_forward_kinematics,
    youbot_jacobian,
)
from portfolio_robotics.planning import make_transform  # noqa: E402


CHECKPOINTS = np.array(
    [
        [0.34, 0.08, 0.28],
        [0.18, -0.16, 0.36],
        [0.41, -0.05, 0.23],
        [0.23, 0.18, 0.31],
    ],
    dtype=float,
)
START_POSITION = np.array([0.12, 0.0, 0.25], dtype=float)
CHECKPOINT_YAWS = np.deg2rad([35.0, -45.0, 10.0, 80.0])
YOUBOT_SAMPLE = np.array([0.15, -0.35, 0.25, -0.20, 0.10], dtype=float)


def rotation_z(yaw: float) -> np.ndarray:
    """Return a 3x3 rotation about the world z-axis."""
    cosine = np.cos(yaw)
    sine = np.sin(yaw)
    return np.array(
        [[cosine, -sine, 0.0], [sine, cosine, 0.0], [0.0, 0.0, 1.0]],
        dtype=float,
    )


def interpolated_checkpoint_path(
    samples_per_segment: int = 25,
) -> tuple[list[int], float, np.ndarray]:
    """Compute the shortest checkpoint order and interpolate every SE(3) segment."""
    order, best_length = shortest_path_order(CHECKPOINTS, START_POSITION)
    ordered_points = CHECKPOINTS[order]
    recomputed_length = path_length(ordered_points, START_POSITION)
    if not np.isclose(best_length, recomputed_length):
        raise RuntimeError("Planning length changed between ordering and verification.")

    current = make_transform(START_POSITION)
    segments: list[np.ndarray] = []
    for checkpoint_index in order:
        target = make_transform(
            CHECKPOINTS[checkpoint_index], rotation_z(CHECKPOINT_YAWS[checkpoint_index])
        )
        segment = interpolate_transform(current, target, samples_per_segment)
        segments.append(segment if not segments else segment[1:])
        current = target

    return order, best_length, np.concatenate(segments, axis=0)


def plot_checkpoint_path(output_path: Path) -> tuple[list[int], float, int]:
    """Plot the true shortest checkpoint route and its interpolated poses."""
    order, best_length, transforms = interpolated_checkpoint_path()
    positions = transforms[:, :3, 3]

    fig = plt.figure(figsize=(12.4, 5.4), constrained_layout=True)
    fig.suptitle("Checkpoint planning from computed SE(3) interpolation", fontsize=15)

    axis_3d = fig.add_subplot(1, 2, 1, projection="3d")
    axis_3d.plot(
        positions[:, 0], positions[:, 1], positions[:, 2], color="#2563eb", linewidth=2.4
    )
    axis_3d.scatter(
        START_POSITION[0],
        START_POSITION[1],
        START_POSITION[2],
        marker="*",
        s=180,
        color="#111827",
        label="Start",
        zorder=5,
    )
    visit_colours = plt.cm.viridis(np.linspace(0.15, 0.9, len(order)))
    for visit, checkpoint_index in enumerate(order, start=1):
        point = CHECKPOINTS[checkpoint_index]
        axis_3d.scatter(*point, s=75, color=visit_colours[visit - 1], zorder=5)
        axis_3d.text(*point, f"  C{checkpoint_index} (#{visit})", fontsize=9)

    # These arrows use rotations returned by interpolate_transform, so the plot
    # also exposes the SLERP orientation component rather than translation alone.
    arrow_indices = np.linspace(0, len(transforms) - 1, 7, dtype=int)
    for index in arrow_indices:
        pose = transforms[index]
        direction = pose[:3, 0]
        axis_3d.quiver(
            *pose[:3, 3],
            *direction,
            length=0.035,
            normalize=True,
            color="#ef4444",
            linewidth=1.1,
            arrow_length_ratio=0.25,
        )

    axis_3d.set_xlabel("x [m]")
    axis_3d.set_ylabel("y [m]")
    axis_3d.set_zlabel("z [m]")
    axis_3d.set_title("3D route and interpolated orientation x-axes")
    axis_3d.legend(loc="upper left")
    axis_3d.view_init(elev=24, azim=-58)
    axis_3d.set_box_aspect((1.2, 1.0, 0.65))
    axis_3d.grid(alpha=0.3)

    axis_xy = fig.add_subplot(1, 2, 2)
    height_plot = axis_xy.scatter(
        positions[:, 0],
        positions[:, 1],
        c=positions[:, 2],
        cmap="plasma",
        s=19,
        zorder=3,
    )
    axis_xy.plot(positions[:, 0], positions[:, 1], color="#64748b", linewidth=1.0)
    axis_xy.scatter(
        START_POSITION[0], START_POSITION[1], marker="*", s=180, color="#111827", zorder=5
    )
    for visit, checkpoint_index in enumerate(order, start=1):
        point = CHECKPOINTS[checkpoint_index]
        axis_xy.scatter(*point[:2], s=75, color=visit_colours[visit - 1], zorder=5)
        axis_xy.annotate(
            f"C{checkpoint_index} (#{visit})",
            point[:2],
            xytext=(6, 6),
            textcoords="offset points",
            fontsize=9,
        )
    colour_bar = fig.colorbar(height_plot, ax=axis_xy, shrink=0.88, pad=0.03)
    colour_bar.set_label("Interpolated z [m]")
    axis_xy.set_xlabel("x [m]")
    axis_xy.set_ylabel("y [m]")
    axis_xy.set_title(
        f"XY projection | order {order} | length {best_length:.4f} m", fontsize=11
    )
    axis_xy.set_aspect("equal", adjustable="datalim")
    axis_xy.grid(alpha=0.25)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180, facecolor="white")
    plt.close(fig)
    return order, best_length, len(transforms)


def plot_youbot_kinematics(output_path: Path) -> tuple[int, float, int]:
    """Plot a real YouBot FK joint sweep and the sample-pose Jacobian."""
    joint_2_values = np.linspace(-1.15, 0.45, 121)
    joint_samples = np.tile(YOUBOT_SAMPLE, (len(joint_2_values), 1))
    joint_samples[:, 1] = joint_2_values
    positions = np.array(
        [youbot_forward_kinematics(joints)[:3, 3] for joints in joint_samples]
    )
    sample_position = youbot_forward_kinematics(YOUBOT_SAMPLE)[:3, 3]
    jacobian = youbot_jacobian(YOUBOT_SAMPLE)
    jacobian_rank = int(np.linalg.matrix_rank(jacobian))
    jacobian_norm = float(np.linalg.norm(jacobian))

    fig = plt.figure(figsize=(12.4, 5.4), constrained_layout=True)
    fig.suptitle("YouBot kinematics computed from the DH model", fontsize=15)

    trajectory_axis = fig.add_subplot(1, 2, 1, projection="3d")
    trajectory_axis.plot(
        positions[:, 0], positions[:, 1], positions[:, 2], color="#334155", linewidth=1.2
    )
    trajectory_points = trajectory_axis.scatter(
        positions[:, 0],
        positions[:, 1],
        positions[:, 2],
        c=joint_2_values,
        cmap="viridis",
        s=18,
        depthshade=False,
    )
    trajectory_axis.scatter(
        *sample_position,
        color="#ef4444",
        marker="*",
        s=180,
        label="Quick-demo pose",
        zorder=5,
    )
    trajectory_colour_bar = fig.colorbar(
        trajectory_points, ax=trajectory_axis, shrink=0.72, pad=0.08
    )
    trajectory_colour_bar.set_label("Joint 2 angle [rad]")
    trajectory_axis.set_xlabel("x [m]")
    trajectory_axis.set_ylabel("y [m]")
    trajectory_axis.set_zlabel("z [m]")
    trajectory_axis.set_title("End-effector trajectory from a joint-2 sweep")
    trajectory_axis.set_box_aspect((1.0, 0.75, 1.0))
    trajectory_axis.view_init(elev=22, azim=-53)
    trajectory_axis.legend(loc="upper left")
    trajectory_axis.grid(alpha=0.3)

    jacobian_axis = fig.add_subplot(1, 2, 2)
    value_limit = float(np.max(np.abs(jacobian)))
    heatmap = jacobian_axis.imshow(
        jacobian,
        cmap="RdBu_r",
        vmin=-value_limit,
        vmax=value_limit,
        aspect="auto",
    )
    for row in range(jacobian.shape[0]):
        for column in range(jacobian.shape[1]):
            value = jacobian[row, column]
            text_colour = "white" if abs(value) > 0.58 * value_limit else "#111827"
            jacobian_axis.text(
                column,
                row,
                f"{value:+.3f}",
                ha="center",
                va="center",
                color=text_colour,
                fontsize=8,
            )
    jacobian_axis.set_xticks(range(5), [f"q{index}" for index in range(1, 6)])
    jacobian_axis.set_yticks(range(6), ["vx", "vy", "vz", "wx", "wy", "wz"])
    jacobian_axis.set_xlabel("Joint")
    jacobian_axis.set_ylabel("End-effector twist component")
    jacobian_axis.set_title(
        f"6x5 Jacobian at quick-demo pose | rank {jacobian_rank} | Frobenius {jacobian_norm:.4f}",
        fontsize=10.5,
    )
    jacobian_colour_bar = fig.colorbar(heatmap, ax=jacobian_axis, shrink=0.88, pad=0.03)
    jacobian_colour_bar.set_label("Jacobian coefficient")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=180, facecolor="white")
    plt.close(fig)
    return len(joint_2_values), jacobian_norm, jacobian_rank


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT_DIR / "docs" / "images",
        help="Directory for generated PNG files (default: docs/images).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    planning_path = args.output_dir / "checkpoint-planning-results.png"
    youbot_path = args.output_dir / "youbot-kinematics-results.png"

    order, length, pose_count = plot_checkpoint_path(planning_path)
    sample_count, jacobian_norm, jacobian_rank = plot_youbot_kinematics(youbot_path)

    print(f"Generated {planning_path}")
    print(f"  shortest order={order}, length={length:.4f} m, interpolated poses={pose_count}")
    print(f"Generated {youbot_path}")
    print(
        f"  FK sweep samples={sample_count}, Jacobian rank={jacobian_rank}, "
        f"Frobenius norm={jacobian_norm:.4f}"
    )


if __name__ == "__main__":
    main()
