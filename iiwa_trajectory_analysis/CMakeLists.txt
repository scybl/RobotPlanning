cmake_minimum_required(VERSION 3.5)
project(iiwa_trajectory_analysis)

find_package(ament_cmake REQUIRED)
find_package(pluginlib REQUIRED)

install(PROGRAMS
  src/trajectory_analysis_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME iiwa_trajectory_analysis
)

install(DIRECTORY launch config urdf bag
  DESTINATION share/${PROJECT_NAME}
  USE_SOURCE_PERMISSIONS
)

install(FILES hardware_interface_plugins.xml
  DESTINATION share/${PROJECT_NAME}
)

install(FILES hardware_interface_plugins.xml
  DESTINATION share/ament_index/resource_index/hardware_interface__pluginlib__plugin
  RENAME ${PROJECT_NAME}
)

ament_package()
