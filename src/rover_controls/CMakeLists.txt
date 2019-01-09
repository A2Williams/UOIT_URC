cmake_minimum_required(VERSION 2.8.3)
project(rover_controls)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  nav_msgs
  roscpp
  rospy
  sensor_msgs
  std_msgs
  rosserial_arduino
  rosserial_client
)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

catkin_package()

rosserial_generate_ros_lib(
  PACKAGE rosserial_arduino
  SCRIPT make_libraries.py
)

rosserial_configure_client(
  DIRECTORY firmware
  TOOLCHAIN_FILE ${ROSSERIAL_ARDUINO_TOOLCHAIN}
)

rosserial_add_client_target(firmware driver ALL)
rosserial_add_client_target(firmware driver-upload)

add_executable(joystick_controller src/joystick_controller.cpp)
target_link_libraries(joystick_controller ${catkin_LIBRARIES})
add_dependencies(joystick_controller rover_controls_generate_messages_cpp)