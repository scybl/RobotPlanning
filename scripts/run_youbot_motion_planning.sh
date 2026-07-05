#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

source_setup() {
  set +u
  # shellcheck disable=SC1090
  source "$1"
  set -u
}

if [[ -f /opt/ros/foxy/setup.bash ]]; then
  source_setup /opt/ros/foxy/setup.bash
fi

SETUP_FILE="$ROOT_DIR/install/setup.bash"
if [[ ! -f "$SETUP_FILE" ]]; then
  echo "Missing $SETUP_FILE. Run: bash scripts/build_workspaces.sh"
  exit 1
fi

source_setup "$SETUP_FILE"
ros2 launch youbot_motion_planning youbot_motion_planning.launch.py rviz:=true trail:=true
