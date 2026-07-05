# Runtime Validation Summary

Date: 2026-07-05

## Commands Tested

```bash
bash scripts/run_project.sh
bash scripts/run_project.sh docker
```

## Result

| Command | Status | Output file |
| --- | --- | --- |
| `bash scripts/run_project.sh` | Passed | `docs/results/run_quick_2026-07-05.txt` |
| `bash scripts/run_project.sh docker` | Passed | `docs/results/run_docker_2026-07-05.txt` |

## Local Quick Run

The local quick run completed successfully with Python 3.11.8 and NumPy 1.26.4. The ROS-free numerical demo reported:

```text
lightweight demo: ok
Jacobian shape/rank  (6, 5) / 5
Ordered path length  0.7969 m
Inertia symmetry err 0.00e+00
```

Local ROS tools were not installed on this macOS environment, which is expected for the quick mode:

```text
ros2: not found (needed only for full RViz/Gazebo runs)
colcon: not found (needed for ROS workspace builds)
```

## Docker ROS Validation

The Docker run built the `robotics-portfolio:foxy` image and validated the ROS 2 Foxy workspace inside the container.

Key results:

```text
ros2: available
colcon: available
rclpy: available
PyKDL: available
xacro: available
Summary: 12 packages finished [22.2s]
Build complete.
```

The IIWA dynamics validation launch finished cleanly:

```text
Case 1:
  fk_rms: 0.000000
  jac_rms: 0.007012
  B_rms: 0.040700
  C_rms: 0.000054
  G_rms: 0.000000
Case 2:
  fk_rms: 0.000000
  jac_rms: 0.007141
  B_rms: 0.032252
  C_rms: 0.000086
  G_rms: 0.000000
process has finished cleanly
```

## Conclusion

The project can be launched through the one-command script. The local quick mode verifies the ROS-free numerical modules, and Docker mode provides a reproducible ROS 2 Foxy build and dynamics validation path.
