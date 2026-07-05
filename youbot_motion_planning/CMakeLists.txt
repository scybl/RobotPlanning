cmake_minimum_required(VERSION 3.5)
project(youbot_motion_planning)

find_package(ament_cmake REQUIRED)

install(PROGRAMS
  src/motion_planner_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME youbot_motion_planner
)

install(FILES
  src/youbot_kdl_utils.py
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY
  launch
  bags
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
