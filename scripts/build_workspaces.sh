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
elif [[ -z "${ROS_DISTRO:-}" ]]; then
  echo "ROS 2 Foxy is not sourced. Run: source /opt/ros/foxy/setup.bash"
  exit 1
fi

command -v colcon >/dev/null 2>&1 || {
  echo "colcon is required. Install python3-colcon-common-extensions."
  exit 1
}

echo "Building root workspace ..."
cd "$ROOT_DIR"
colcon build --symlink-install

echo "Build complete."
