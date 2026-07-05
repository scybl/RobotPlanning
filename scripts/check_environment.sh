#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "Project root: $ROOT_DIR"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3: missing"
  exit 1
fi

echo "python3: $(python3 --version)"
python3 - <<'PY'
import numpy
print(f"numpy: {numpy.__version__}")
PY

echo
echo "Running ROS-free lightweight demo..."
python3 -B demos/lightweight_demo.py >/dev/null
echo "lightweight demo: ok"

echo
if command -v ros2 >/dev/null 2>&1; then
  echo "ros2: $(ros2 --version 2>/dev/null || echo available)"
else
  echo "ros2: not found (needed only for full RViz/Gazebo runs)"
fi

if command -v colcon >/dev/null 2>&1; then
  echo "colcon: available"
else
  echo "colcon: not found (needed for ROS workspace builds)"
fi

python3 - <<'PY'
optional = ["rclpy", "PyKDL", "xacro"]
for name in optional:
    try:
        __import__(name)
        print(f"{name}: available")
    except Exception:
        print(f"{name}: not found")
PY
