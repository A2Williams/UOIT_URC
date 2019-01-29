#!/usr/bin/env python

# Copyright 2017, Digi International Inc.
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
import rospy
import base64

# TODO: Replace with the serial port where your local module is connected to.

# TODO: Replace with the baud rate of your local module.
PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200

from digi.xbee.devices import XBeeDevice
from std_msgs.msg import String

with open("test_image.jpg", "rb") as imageFile:
    image_str = base64.b64encode(imageFile.read())
    print(image_str)


DATA_TO_SEND = "Sent_Data"
REMOTE_NODE_ID = "REMOTE"

MAX_DATA_RATE = 255



def main():
    print(" +--------------------------------------+")
    print(" | XBee Python Library Send Data Sample |")
    print(" +--------------------------------------+\n")
    pub = rospy.Publisher('chatter', String, queue_size=10) #
    rospy.init_node('talker', anonymous=True) #
    rate = rospy.Rate(1000) # 10hz
    device = XBeeDevice(PORT, BAUD_RATE)
    counter = 0
    device.open()
    while not rospy.is_shutdown(): #
        hello_str = "hello world %s" % rospy.get_time() #
        rospy.loginfo(hello_str) #
        pub.publish(hello_str) #
        while (counter < len(image_str)) and ((len(image_str) - counter) > MAX_DATA_RATE):
            device.send_data_broadcast(image_str[counter:(counter + MAX_DATA_RATE)])
            counter = counter + MAX_DATA_RATE
        print("Success")
	rate.sleep() #
    device.close()




    #try:
    #    device.open()

    #    device.send_data_broadcast(DATA_TO_SEND)

    #   print("Success")

    #finally:
        #if device is not None and device.is_open():
        #    device.close()

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

if __name__ == '__main__':
    try:
        #talker()
        main()
    except rospy.ROSInterruptException:
        pass
