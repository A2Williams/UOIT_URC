#How to launch rtabmap using Zed

To use the Zed stereo camera for creating a map using rtabmap, enter the following commands to launch the rtabmap node and visualizer:

There are two options to launch the rtabmap, one uses the odometry created within the rtabmap node using visual landmarks,
and the other uses the Zed's odometry topic. 
The following code was gathered from the [rtabmap_ros package] (http://wiki.ros.org/rtabmap_ros/Tutorials/HandHeldMapping).

### If using the odometry from rtabmap:
```
$ export ROS_NAMESPACE=camera
$ roslaunch zed_wrapper zed_camera.launch publish_tf:=false
```
This launches the zed camera node. Now we can run the algorithm and visualizer:
```
$ roslaunch rtabmap_ros rtabmap.launch rtabmap_args:="--delete_db_on_start" depth_topic:=/camera/depth/depth_registered frame_id:=zed_camera_center approx_sync:=false
```

### If using Zed odometry:
```
$ export ROS_NAMESPACE=camera
$ roslaunch zed_wrapper zed_camera.launch publish_map_tf:=false
$ roslaunch rtabmap_ros rtabmap.launch rtabmap_args:="--delete_db_on_start" depth_topic:=/camera/depth/depth_registered frame_id:=zed_camera_center approx_sync:=false visual_odometry:=false odom_topic:=/camera/odom
```

This creates a 3D pointcloud with depth info to be used for navigation.
