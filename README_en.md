# RobotPlanning

[中文](README.md)

RobotPlanning is a ROS 2 robotics planning and dynamics workspace. It includes YouBot kinematics, path planning, inverse-kinematics trajectories, and KUKA IIWA14 dynamics validation.

![RobotPlanning preview](docs/images/robot-planning-preview.svg)

## Features

- Provides quaternion conversion, YouBot forward kinematics, and Jacobian calculation.
- Implements checkpoint ordering, SE(3) interpolation, and inverse-kinematics trajectory generation.
- Includes IIWA14 dynamics modelling, acceleration analysis, and validation scripts.
- Supports a ROS-free numerical demo, Docker builds, and local ROS runs.

## Results

| Item | Result |
| --- | --- |
| YouBot Jacobian | shape/rank = `(6, 5) / 5` |
| Checkpoint path | 0.7969 m |
| IIWA inertia symmetry error | 0.00e+00 |
| Supported modes | quick / docker / ros-build |

## Quick Start

ROS-free quick demo:

```bash
bash scripts/run_project.sh quick
```

Reuse an existing conda environment:

```bash
conda run -n codex_python bash scripts/run_project.sh quick
```

Docker validation:

```bash
bash scripts/run_project.sh docker
```

## Requirements

- Quick demo: Python 3 + NumPy
- Full ROS run: Ubuntu 20.04 + ROS 2 Foxy
- Optional: Docker, RViz, Gazebo, MoveIt 2

## Data Notes

The project does not require an external dataset. `docs/results/` stores sample run logs, and `docs/reports/` stores reference reports.

## Project Layout

```text
portfolio_robotics/        ROS-free algorithm wrappers
demos/                     Lightweight numerical demo
youbot_*                   YouBot kinematics, simulation, and visualisation packages
iiwa_*                     IIWA dynamics, Gazebo, and MoveIt packages
robot_description/         YouBot model files
scripts/                   Run, check, and build scripts
docker/                    ROS 2 Foxy Docker environment
docs/                      Results and reports
```

## Tests

```bash
pytest tests/ -q
```
