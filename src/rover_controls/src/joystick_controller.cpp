//Includes for a ROS CPP file
#include "ros/ros.h"
#include "std_msgs/String.h"
#include "ros/time.h"

//Includes for each of the message types we will be using
#include <std_msgs/Int16.h>
#include <sensor_msgs/Joy.h>

#include <cmath>

std_msgs::Int16 left_drive; //Our motor voltage to be calculated
std_msgs::Int16 right_drive;
sensor_msgs::Joy joystick_msg; //our range msg inputted

//This assumes that the max voltage is 23, this was just to get some
//extra resolution on the float values.

float JOY_MAX = 1;
float VAL_RANGE = 64;
int MAX_VAL = 256;
int MID_VAL = 192;
int MIN_VAL = 128; 
int breakOn;
float joy_x;
float joy_y;
float twist_angle;

//This callback pulls values from our subscribed message (range_msg)
//and assigns it to a local variable encoder_pos
void joy_callback(const sensor_msgs::Joy &joystick_msg)
{
  joy_x = joystick_msg.axes[0];
  joy_y = joystick_msg.axes[3];
  twist_angle = joystick_msg.axes[2];
  breakOn = joystick_msg.buttons[3];
}


int main(int argc, char **argv)
{

  //initialize our controller node
  ros::init(argc, argv, "control_node");

  // Create node handle
  ros::NodeHandle nh;

  //Set up publisher and Subscriber
  //Publish to topic "drive"
  //Subscribe to topic "joy"
  ros::Publisher left_drive_pub = nh.advertise<std_msgs::Int16>("left_drive", 10);
  ros::Publisher right_drive_pub = nh.advertise<std_msgs::Int16>("right_drive", 10);
  ros::Subscriber joy_sub = nh.subscribe("joy", 10, joy_callback);
  //Determine publish and subscribe rate
  ros::Rate loop_rate(10);

  ROS_INFO("Joystick Controller Node Initialized, Drive Safe!");
  //while node active (terminal active)
  while (ros::ok())
  {

    //Some kind of differential drive steering
    if(breakOn != 1) {
      left_drive.data = 0;
      right_drive.data = 0;
    }
    else {
      int x_joy_pos = (joy_x  * VAL_RANGE);
      int y_joy_pos = (-joy_y  * VAL_RANGE);


      int left_val = MID_VAL + (x_joy_pos + y_joy_pos); 
      int right_val = MID_VAL - (x_joy_pos + y_joy_pos);

      if (left_val > MAX_VAL) {
        left_val = MAX_VAL;
      }
      if (left_val < MIN_VAL) {
        left_val = MIN_VAL;
      }
      if (right_val > MAX_VAL) {
        right_val = MAX_VAL;
      }
      if (right_val < MIN_VAL) {
        right_val = MIN_VAL;
      }

      left_drive.data = left_val;
      right_drive.data = right_val;
    }

	  left_drive_pub.publish(left_drive);
    right_drive_pub.publish(right_drive);

    //
    ros::spinOnce();

    //This term ensures we are publishing and subscribing at the right rate
    loop_rate.sleep();
  }


  return 0;
}
