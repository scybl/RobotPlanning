# Runtime Validation Summary

Date: 2026-08-09

## Commands Tested

```bash
bash scripts/run_project.sh quick
pytest tests/ -q
```

## Local Quick Run

The local quick run completed successfully with Python 3.12.11 and NumPy 2.5.1. The ROS-free numerical demo reported:

```text
lightweight demo: ok
Jacobian shape/rank  (6, 5) / 5
Ordered path length  0.7969 m
Inertia symmetry err 0.00e+00
```

ROS tools were not installed in the local macOS shell used for this quick run, which is expected for the quick mode:

```text
ros2: not found (needed only for full RViz/Gazebo runs)
colcon: not found (needed for ROS workspace builds)
```

## Result Assets

| Asset | Purpose |
| --- | --- |
| `docs/results/run_quick_2026-08-09.txt` | Sanitised quick-run output |
| `docs/images/planning-quick-run.svg` | README quick-run visual |
| `docs/images/planning-stack-run.svg` | README ROS stack visual |

## Conclusion

Quick mode verifies the numerical modules without ROS. Full RViz, Gazebo, MoveIt 2, and IIWA validation paths remain available through `scripts/run_project.sh` modes on a ROS 2 Foxy environment or through the Docker validation path.
