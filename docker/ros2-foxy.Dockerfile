FROM osrf/ros:foxy-desktop

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-colcon-common-extensions \
    python3-matplotlib \
    python3-numpy \
    python3-pykdl \
    ros-foxy-gazebo-ros-pkgs \
    ros-foxy-gazebo-ros2-control \
    ros-foxy-joint-state-publisher-gui \
    ros-foxy-moveit \
    ros-foxy-robot-state-publisher \
    ros-foxy-ros2-control \
    ros-foxy-ros2-controllers \
    ros-foxy-rviz2 \
    ros-foxy-xacro \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace/RobotPlanning
COPY . .

RUN python3 demos/lightweight_demo.py

CMD ["/bin/bash"]
