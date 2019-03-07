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
import struct

# TODO: Replace with the serial port where your local module is connected to.

# TODO: Replace with the baud rate of your local module.
PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200

from digi.xbee.devices import XBeeDevice
from std_msgs.msg import String
from sensor_msgs.msg import Joy

DATA_TO_SEND = "Sent_Data"
REMOTE_NODE_ID = "REMOTE"
x_direc = 0x00000000
y_direc = 0x00000000
vel_mag = 0x00000000
checksum = 0x00000000
MAX_DATA_RATE = 255
global VELOCITY_DATA
VELOCITY_DATA = '00000000000000000000000000000000'

def callback(data):
    global VELOCITY_DATA

    vel_mag = float_to_hex(data.axes[3]) #Velocity magnitude (Rocker)
    x_direc = float_to_hex(data.axes[0]) #X_direction (Right Joy L/R)
    y_direc = float_to_hex(data.axes[1]) #Y direction (right Joy F/B)
	
    #Currently Unused joystick operations::
    extra_1 = float_to_hex(data.axes[2]) #Extra data for joy
    extra_2 = float_to_hex(data.axes[4]) #Extra data for joy

    # Button layout: [0 1 2 3 4 5 6 7] "buttons" is a binary array
    buttons = [0, 0, 0, 0, 0, 0, 0, 0]
    butttons[0:8] = data.buttons[0:8] #Grab first 8 buttons from joystick
    buttons_str = ‘’.join(map(str, buttons))
    buttons_hex = hex(int(buttons_str,2))	
    
    checksum = float_to_hex(data.axes[3]+data.axes[0]+data.axes[1])
    VELOCITY_DATA = str(vel_mag[2:])+str(x_direc[2:])+str(y_direc[2:])+str(checksum[2:])


def main():
    global VELOCITY_DATA
    print(" +--------------------------------------+")
    print(" |    XBee Python ROS Broadcast Node    |")
    print(" +--------------------------------------+\n")

    rospy.init_node('teleop_comms',anonymous=True)
    rospy.Subscriber("joy", Joy, callback)
    rate = rospy.Rate(1000) # 10hz
    device = XBeeDevice(PORT, BAUD_RATE)

    device.open()

    while not rospy.is_shutdown():
        
        device.send_data_broadcast(VELOCITY_DATA)
        
	rate.sleep() #
    device.close()

def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
