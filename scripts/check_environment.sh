#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "Project root: $ROOT_DIR"
DEFAULT_PYTHON_BIN="python3"
if [[ -n "${CONDA_PREFIX:-}" && -x "${CONDA_PREFIX}/bin/python" ]]; then
  DEFAULT_PYTHON_BIN="${CONDA_PREFIX}/bin/python"
fi
PYTHON_BIN="${PYTHON_BIN:-$DEFAULT_PYTHON_BIN}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
  echo "$PYTHON_BIN: missing"
  exit 1
fi

echo "$PYTHON_BIN: $("$PYTHON_BIN" --version)"
"$PYTHON_BIN" - <<'PY'
import numpy
print(f"numpy: {numpy.__version__}")
PY

echo
echo "Running ROS-free lightweight demo..."
"$PYTHON_BIN" -B demos/lightweight_demo.py >/dev/null
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

"$PYTHON_BIN" - <<'PY'
optional = ["rclpy", "PyKDL", "xacro"]
for name in optional:
    try:
        __import__(name)
        print(f"{name}: available")
    except Exception:
        print(f"{name}: not found")
PY
