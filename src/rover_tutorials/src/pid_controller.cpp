//Includes for a ROS CPP file
#include "ros/ros.h"
#include "std_msgs/String.h"
#include "ros/time.h"

//Includes for each of the message types we will be using
#include <std_msgs/Float64.h>
#include <sensor_msgs/Range.h>
#include <sstream>

//Using the namespace for the useg message classes
using namespace sensor_msgs;
using namespace std_msgs;

std_msgs::Float64 motor_voltage_input; //Our motor voltage to be calculated
sensor_msgs::Range range_msg; //our range msg inputted
float encoder_pos; //our encoder position from our range input
float actual_pos; //our actual position taking into account en
float desired_pos = 210; //desired position
float error = 0;
float previous_error;
float total_error;

//Gains for PID controller
float kp = 1; //Proportional Gain
float ki = 0; //Integral Gain
float kd = 0; //Derivative Gain

//This callback pulls values from our subscribed message (range_msg)
//and assigns it to a local variable encoder_pos
void range_callback(const sensor_msgs::Range &range_msg)
{
	encoder_pos = range_msg.max_range;
}


int main(int argc, char **argv)
{

  //initialize our controller node
  ros::init(argc, argv, "control_node");

  // Create node handle
  ros::NodeHandle nh;

  //Set up publisher and Subscriber
  //Publish to topic "motor_voltage"
  //Subscribe to topic "range_data"
  ros::Publisher motor_pub = nh.advertise<std_msgs::Float64>("motor_voltage", 500);
  ros::Subscriber range_sub = nh.subscribe("range_data", 500, range_callback);
  //Determine publish and subscribe rate
  ros::Rate loop_rate(500);

  //while node active (terminal active)
  while (ros::ok())
  {
    //PID controller
    actual_pos = encoder_pos; //depending on tics/rev (70 pulse per rev)::do math
    previous_error = error; //This is for derivative calculations
    error = desired_pos - actual_pos; //This is the error between desired and real
    total_error += error; //This is for integral gain ki (sum of error over time)

    // Now the actual Controller
    //Multiply kp by proportional error, kd by derivative error and ki by error sum
    motor_voltage_input.data = (kp*error) + (kd*(error - previous_error)) + (ki*total_error);

    //now that we have a proposed input (voltage), lets publish it to the topic
	  motor_pub.publish(motor_voltage_input);

    //
    ros::spinOnce();

    //This term ensures we are publishing and subscribing at the right rate
    loop_rate.sleep();
  }


  return 0;
}
