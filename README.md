# Robotics Kinematics, Dynamics, and Motion Planning Suite

[中文说明](README.zh-CN.md)

This repository packages a robotics kinematics, planning, and dynamics stack into one root-level ROS 2 workspace. The code demonstrates rigid-body rotation conversion, mobile-manipulator kinematics, Jacobian computation, checkpoint path planning, inverse kinematics, and IIWA dynamics validation.

The project is organised as one workspace with related package groups:

| Package group | Packages | Focus |
| --- | --- | --- |
| YouBot kinematics and ROS services | `quaternion_conversion`, `quaternion_conversion_interfaces`, `youbot_fk_broadcaster`, `youbot_kinematics` | Quaternion services, DH forward kinematics, YouBot frame broadcasting, Jacobian checks |
| Planning and dynamics | `youbot_motion_planning`, `iiwa_dynamics`, `iiwa_trajectory_analysis` | YouBot checkpoint ordering, SE(3) interpolation, position-only IK, IIWA dynamics and acceleration analysis |
| Shared robot assets | `robot_description`, `youbot_simulator`, `youbot_trail_visualizer`, `iiwa_ros2_gazebo`, `iiwa_ros2_moveit2` | URDF/Xacro models, RViz configs, Gazebo launch files, and MoveIt 2 configuration |

## Highlights

- ROS 2 service nodes for quaternion-to-Euler and quaternion-to-Rodrigues conversion.
- Denavit-Hartenberg forward kinematics for the KUKA YouBot arm, including URDF offset and joint-polarity alignment.
- Analytical YouBot Jacobian with KDL-compatible frame conventions.
- Brute-force shortest checkpoint ordering, transform interpolation with quaternion SLERP, and position-only inverse kinematics.
- Manual IIWA14 forward kinematics, centre-of-mass Jacobians, inertia matrix, Coriolis term, gravity vector, and KDL-oriented validation.
- A lightweight NumPy demo that runs without ROS 2 for quick project verification.

## Repository Layout

```text
.
|-- quaternion_conversion/             # Quaternion conversion service node
|-- quaternion_conversion_interfaces/  # Custom service definitions
|-- youbot_fk_broadcaster/             # YouBot forward-kinematics TF broadcaster
|-- youbot_kinematics/                 # YouBot FK and Jacobian implementation
|-- youbot_motion_planning/            # YouBot checkpoint planning and IK trajectory
|-- iiwa_dynamics/                     # IIWA14 dynamics implementation and validation
|-- iiwa_trajectory_analysis/          # IIWA trajectory playback and acceleration analysis
|-- robot_description/                 # YouBot description package
|-- youbot_simulator/                  # YouBot RViz/Gazebo support package
|-- youbot_trail_visualizer/           # RViz trail visualiser
|-- iiwa_ros2_gazebo/                  # IIWA Gazebo package
|-- iiwa_ros2_moveit2/                 # IIWA MoveIt 2 package
|-- portfolio_robotics/                # ROS-free algorithm wrappers used by the quick demo
|-- demos/lightweight_demo.py          # Deterministic terminal demo requiring only Python + NumPy
|-- scripts/run_project.sh             # One-command entry point for local and Docker runs
|-- scripts/                           # Environment checks, workspace build, ROS launch helpers
|-- docs/reports/                      # Reference PDF reports retained as project artifacts
|-- docs/results/                      # Captured sample outputs
|-- docker/ros2-foxy.Dockerfile        # Optional reproducible ROS 2 Foxy environment
```

Generated ROS folders such as `build/`, `install/`, and `log/` are ignored by git.

## One-Command Start

For a fast local check that only needs Python 3 and NumPy:

```bash
bash scripts/run_project.sh
```

For a reproducible full ROS 2 build and terminal validation in Docker:

```bash
bash scripts/run_project.sh docker
```

Available modes:

| Command | Purpose |
| --- | --- |
| `bash scripts/run_project.sh` | Local environment check plus ROS-free numerical demo |
| `bash scripts/run_project.sh docker` | Build the Docker image, build the ROS workspace, and run IIWA dynamics validation |
| `bash scripts/run_project.sh ros-build` | Build the root workspace on a local ROS 2 Foxy environment |
| `bash scripts/run_project.sh iiwa-validation` | Build if needed, then run IIWA dynamics validation |
| `bash scripts/run_project.sh youbot-fk` | Build if needed, then launch the YouBot forward-kinematics RViz demo |
| `bash scripts/run_project.sh youbot-planning` | Build if needed, then launch the YouBot motion-planning RViz demo |

## Quick Demo Without ROS

Use this when you want to verify the project on a normal Python environment:

```bash
bash scripts/run_project.sh quick
```

Expected output includes quaternion conversion, YouBot FK/Jacobian values, checkpoint ordering, and IIWA dynamics diagnostics. A captured run is stored in `docs/results/lightweight_demo.txt`.

You can also run the lightweight environment check:

```bash
bash scripts/check_environment.sh
```

## ROS 2 Environment

The ROS workspace targets ROS 2 Foxy on Ubuntu 20.04. A full visualization setup should provide:

- ROS 2 Foxy desktop tools: `ros2`, `rviz2`, `xacro`, `robot_state_publisher`
- `colcon` and `ament_cmake`
- Python packages: `numpy`, `PyKDL`, `matplotlib`
- ROS packages for joint state GUI, Gazebo integration, ros2_control, and MoveIt 2 when running the IIWA simulation stack

Optional Docker environment:

```bash
bash scripts/run_project.sh docker
```

The Docker mode builds the image, runs the environment check, builds the workspace, and executes the IIWA dynamics validation. It uses `linux/amd64` by default for ROS 2 Foxy image compatibility. You can override the image tag or platform:

```bash
DOCKER_IMAGE=my-robotics-stack:foxy bash scripts/run_project.sh docker
DOCKER_PLATFORM=linux/amd64 bash scripts/run_project.sh docker
```

For local Ubuntu/ROS usage, source ROS 2 first and build the root workspace:

```bash
source /opt/ros/foxy/setup.bash
bash scripts/run_project.sh ros-build
```

## Full ROS Runs

After building, each helper script sources `install/setup.bash` from the root workspace and launches a focused demo.

YouBot forward kinematics in RViz:

```bash
bash scripts/run_project.sh youbot-fk
```

YouBot checkpoint path planning and trajectory visualization:

```bash
bash scripts/run_project.sh youbot-planning
```

IIWA dynamics validation against the KDL reference implementation:

```bash
bash scripts/run_project.sh iiwa-validation
```

## Runtime Validation

The one-command entry points were tested on 2026-07-05. The captured logs are stored in `docs/results/`:

| Command | Status | Log |
| --- | --- | --- |
| `bash scripts/run_project.sh` | Passed | `docs/results/run_quick_2026-07-05.txt` |
| `bash scripts/run_project.sh docker` | Passed | `docs/results/run_docker_2026-07-05.txt` |

Validation summary:

- Local quick mode completed the environment check and ROS-free numerical demo.
- Docker mode built the `robotics-portfolio:foxy` image, built 12 ROS packages, and completed IIWA dynamics validation cleanly.
- A short combined report is available at `docs/results/run_validation_summary_2026-07-05.md`.

## Sample Results

The lightweight demo reports deterministic numerical checks, for example:

```text
Quaternion demo
  Euler ZYX [rad]      roll=+0.0000 pitch=+0.7854 yaw=+0.0000
  Rodrigues vector     [+0.0000, +0.4142, +0.0000]

YouBot kinematics demo
  End-effector xyz [m]  [-0.0378, +0.0330, +0.4490]
  Jacobian shape/rank   (6, 5) / 5

IIWA dynamics demo
  Inertia symmetry err  0.00e+00
```

The ROS demos provide richer visual output in RViz/Gazebo using the included robot descriptions, launch files, and bag data.
