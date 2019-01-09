#if defined(ARDUINO) && ARDUINO >= 100
  #include <Arduino.h>
#else
  #include <WProgram.h>
#endif

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <ros.h>
#include <std_msgs/Int16.h>


Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

ros::NodeHandle nh;

// callback messages for left and right side of the drive
void lDrive_cb(const std_msgs::Int16& cmd_msg) {
  if (cmd_msg.data == 0 || cmd_msg.data == 192) {
    pwm.setPWM(0,0,0);
  }
  else {
    pwm.setPWM(0,0,cmd_msg.data);
  }
}

void rDrive_cb(const std_msgs::Int16& cmd_msg) {
  if (cmd_msg.data == 0 || cmd_msg.data == 192) {
  }
  else {
  }
}

ros::Subscriber<std_msgs::Int16> left_pos("left_drive", &lDrive_cb);
ros::Subscriber<std_msgs::Int16> right_pos("right_drive", &rDrive_cb);

void setup() {
  nh.initNode();
  nh.subscribe(left_pos);
  nh.subscribe(right_pos);

  pwm.begin();
  // frequency calculation for a 256 bit range 
  float freq = 1E6 / (7.8125 * 4096);
  pwm.setPWMFreq(freq);
}

void loop() {
  nh.spinOnce();
  delay(1);
}