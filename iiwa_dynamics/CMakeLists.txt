cmake_minimum_required(VERSION 3.5)
project(iiwa_dynamics)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)

ament_python_install_package(${PROJECT_NAME} PACKAGE_DIR src/${PROJECT_NAME})

install(FILES
  model.urdf
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY resource
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

install(PROGRAMS
  src/iiwa_dynamics/validation_node.py
  DESTINATION lib/${PROJECT_NAME}
  RENAME iiwa_dynamics_validator
)

ament_package()
