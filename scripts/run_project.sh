#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

DOCKER_IMAGE="${DOCKER_IMAGE:-robotics-portfolio:foxy}"
DOCKER_PLATFORM="${DOCKER_PLATFORM:-linux/amd64}"
DEFAULT_PYTHON_BIN="python3"
if [[ -n "${CONDA_PREFIX:-}" && -x "${CONDA_PREFIX}/bin/python" ]]; then
  DEFAULT_PYTHON_BIN="${CONDA_PREFIX}/bin/python"
fi
PYTHON_BIN="${PYTHON_BIN:-$DEFAULT_PYTHON_BIN}"
MODE="${1:-quick}"

usage() {
  cat <<'EOF'
Usage:
  bash scripts/run_project.sh [mode]

Modes:
  quick             Run the local environment check and ROS-free numerical demo.
  docker            Build the ROS 2 Foxy Docker image, then build and validate the ROS workspace inside it.
  ros-build         Build the root ROS 2 workspace on a local ROS 2 Foxy environment.
  iiwa-validation   Build if needed, then run IIWA dynamics validation.
  youbot-fk         Build if needed, then launch the YouBot forward-kinematics RViz demo.
  youbot-planning   Build if needed, then launch the YouBot motion-planning RViz demo.
  help              Show this help message.

Environment overrides:
  DOCKER_IMAGE      Docker image tag, default: robotics-portfolio:foxy
  DOCKER_PLATFORM   Docker platform, default: linux/amd64
  PYTHON_BIN         Python executable for quick local checks, default: python3
EOF
}

require_command() {
  local command_name="$1"
  local install_hint="$2"

  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "Missing command: $command_name"
    echo "$install_hint"
    exit 1
  fi
}

ensure_ros_workspace_built() {
  if [[ ! -f "$ROOT_DIR/install/setup.bash" ]]; then
    echo "No local install/setup.bash found. Building the ROS workspace first..."
    bash scripts/build_workspaces.sh
  fi
}

run_quick() {
  echo "== Environment check =="
  bash scripts/check_environment.sh

  echo
  echo "== Lightweight numerical demo =="
  "$PYTHON_BIN" -B demos/lightweight_demo.py
}

run_docker() {
  require_command docker "Install Docker Desktop or Docker Engine, then rerun this command."

  echo "== Building Docker image: $DOCKER_IMAGE ($DOCKER_PLATFORM) =="
  docker build \
    --platform "$DOCKER_PLATFORM" \
    -f docker/ros2-foxy.Dockerfile \
    -t "$DOCKER_IMAGE" \
    .

  echo
  echo "== Building and validating the ROS workspace inside Docker =="
  docker run --rm \
    --platform "$DOCKER_PLATFORM" \
    "$DOCKER_IMAGE" \
    bash -lc 'bash scripts/check_environment.sh && bash scripts/build_workspaces.sh && bash scripts/run_iiwa_dynamics_validation.sh'
}

case "$MODE" in
  quick)
    run_quick
    ;;
  docker)
    run_docker
    ;;
  ros-build)
    bash scripts/build_workspaces.sh
    ;;
  iiwa-validation)
    ensure_ros_workspace_built
    bash scripts/run_iiwa_dynamics_validation.sh
    ;;
  youbot-fk)
    ensure_ros_workspace_built
    bash scripts/run_youbot_fk_broadcaster.sh
    ;;
  youbot-planning)
    ensure_ros_workspace_built
    bash scripts/run_youbot_motion_planning.sh
    ;;
  help|-h|--help)
    usage
    ;;
  *)
    echo "Unknown mode: $MODE"
    echo
    usage
    exit 1
    ;;
esac
