# UOIT_URC18
Catkin workspace for UOIT's rover system 

### Prerequisites
You must have ROS Kinetic installed on your Ubuntu 16.04 platform.

### Installing the workspace on your machine.
First you need to download the repository to your home directory. Open up a new terminal and enter the following commands:

```
cd ~
git clone https://github.com/A2Williams/UOIT_URC.git
```
You should now have a folder named UOIT_URC in your home directory.

Now we have to build the workspace. To do this, you may have to delete the build and devel folders inside the workspace. To do this, enter the workspace:
```
cd UOIT_URC
```
Confirm you are in the workspace by entering the following into the terminal:
```
ls
```
You should see three folders. /build, /devel, and /src. This means you are in the right folder. Remove the /build and /devel folders by entering:
```
sudo rm -r build
sudo rm -r devel
```
You are now ready to compile the workspace. Enter the following commands to build the workspace: Note - we should be in the ~/UOIT_URC/ folder. 

```
catkin_make
source devel/setup.bash
```

Now we have our compiled workspace and should be able to run the rover's systems on our personal devices. 

To upload to the Motor control Node run:
```
catkin_make rover_controls_firmware_driver-upload
```
to run the Motor control Node you must run:
```
rosrun rosserial_python serial_node.py /dev/ttyACM0
```
the last parameter `/dev/ttyACM0` is the USB port the Arduino is connected to and my not be the same on your system.