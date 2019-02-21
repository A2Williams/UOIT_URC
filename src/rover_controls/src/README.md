# Uploading to Arduino

To upload the Motor control Node to the arduino run:
```
catkin_make rover_controls_firmware_driver-upload
```
# Node Startup
In addition to running `roscore`, to run the Motor control Node you must start the `joy_node` and `/joy` topic the `joystick_controller`node which starts the `/left_drive` and `/right_drive`, and the `serial_node` from `rosserial_python` :
```
rosrun joy joy_node

rosrun rover_controls joystick_controller

rosrun rosserial_python serial_node.py /dev/ttyACM0
```

the last parameter `/dev/ttyACM0` is the USB port the Arduino is connected to and my not be the same on your system.