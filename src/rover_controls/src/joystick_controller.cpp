//Includes for a ROS CPP file
#include "ros/ros.h"
#include "std_msgs/String.h"
#include "ros/time.h"

//Includes for each of the message types we will be using
#include <std_msgs/Float64.h>
#include <sensor_msgs/Joy.h>
#include <sstream>

//Using the namespace for the useg message classes
using namespace sensor_msgs;
using namespace std_msgs;

std_msgs::Float64 left_motor_voltage; //Our motor voltage to be calculated
std_msgs::Float64 right_motor_voltage;
sensor_msgs::Joy joystick_msg; //our range msg inputted

//This assumes that the max voltage is 23, this was just to get some
//extra resolution on the float values.

float max_voltage = 23; //23V max voltage
float velocity_magnitude;
float velocity_direction;
float twist_angle;
//This callback pulls values from our subscribed message (range_msg)
//and assigns it to a local variable encoder_pos
void joy_callback(const sensor_msgs::Joy &joystick_msg)
{
	velocity_magnitude = joystick_msg.axes[2];
  velocity_direction = joystick_msg.axes[1];
  twist_angle = joystick_msg.axes[3];
}


int main(int argc, char **argv)
{

  //initialize our controller node
  ros::init(argc, argv, "control_node");

  // Create node handle
  ros::NodeHandle nh;

  //Set up publisher and Subscriber
  //Publish to topic "motor_voltage"
  //Subscribe to topic "joy"
  ros::Publisher left_motor_pub = nh.advertise<std_msgs::Float64>("left_motor_voltage", 500);
  ros::Publisher right_motor_pub = nh.advertise<std_msgs::Float64>("right_motor_voltage", 500);
  ros::Subscriber joy_sub = nh.subscribe("joy", 500, joy_callback);
  //Determine publish and subscribe rate
  ros::Rate loop_rate(500);

  ROS_INFO("Joystick Controller Node Initialized, Drive Safe!");
  //while node active (terminal active)
  while (ros::ok())
  {

    //Some kind of differential drive steering
    if(velocity_magnitude == 0) {
      left_motor_voltage.data = 0;
      right_motor_voltage.data = 0;
    }
    else {
      left_motor_voltage.data = (velocity_direction*(velocity_magnitude*max_voltage))-0.2*(twist_angle*max_voltage);
      right_motor_voltage.data = (velocity_direction*(velocity_magnitude*max_voltage))+0.2*(twist_angle*max_voltage);
    }

	  left_motor_pub.publish(left_motor_voltage);
    right_motor_pub.publish(right_motor_voltage);

    //
    ros::spinOnce();

    //This term ensures we are publishing and subscribing at the right rate
    loop_rate.sleep();
  }


  return 0;
}
