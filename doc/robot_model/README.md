Author: Abhi Patel
Date:02/25/19
Email: abhi.patel@uoit.net 

###Usage:
```
$ roslaunch rover_description rover.launch
```
Notes:
- Add proper inertial values to fix glitchy wheels in gazebo and rviz
- Write a 6-wheeled drive plugin for gazebo


###To generate a urdf from the xacro, navigate to UOIT_URC/src/rover_description/urdf/ and execute:
```
$ rosrun xacro xacro --inorder -o generated_model.urdf rover_model.urdf.xacro
```
 
###To control the gazebo model that uses the differential drive plugin:
```
$ rosrun teleop_twist_keyboard teleop_twist_keyboard.py
```

 *Use ctrl-c and ctrl-z to exit gazebo
 
 