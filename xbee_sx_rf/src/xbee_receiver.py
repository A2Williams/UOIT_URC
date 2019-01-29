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
import binascii

# TODO: Replace with the serial port where your local module is connected to.

# TODO: Replace with the baud rate of your local module.
PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200

from digi.xbee.devices import XBeeDevice
from std_msgs.msg import String
from std_msgs.msg import Int16
global msg

def hexint(b):
    return int(binascii.hexlify(b),16)

def main():
    print(" +--------------------------------------+")
    print(" |        XBee Receive Data Node        |")
    print(" +--------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)

    pub = rospy.Publisher('left_drive', Int16, queue_size=10) #
    rospy.init_node('teleop_comms', anonymous=True) #
    rate = rospy.Rate(1000) # 1000hz to be changed later if needed


    device.open()
    msg = 0
    while not rospy.is_shutdown():
        def data_receive_callback(xbee_message):
            #l_drive = xbee_message.data.decode()
            l_drive = xbee_message.data
            msg = hexint(l_drive)
            #print(msg)
            pub.publish(Int16(msg))

        device.add_data_received_callback(data_receive_callback)
        print("Waiting for data...\n")
        #pub.publish(msg)
        rospy.spin()
        rate.sleep() #

	print("*******Closing Device************")
    device.close()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
