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
import struct

# TODO: Replace with the serial port where your local module is connected to.

# TODO: Replace with the baud rate of your local module.
PORT = "/dev/ttyUSB0"
#You may have to change the PORT or BAUD in devices.py as well
BAUD_RATE = 115200

from digi.xbee.devices import XBeeDevice
from std_msgs.msg import String
from std_msgs.msg import Int16
from sensor_msgs.msg import Joy
global msg

def hexint(b):
    return int(binascii.hexlify(b),16)

def main():
    print(" +--------------------------------------+")
    print(" |        XBee Receive Data Node        |")
    print(" +--------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)

    pub = rospy.Publisher('joy', Joy, queue_size=10) #
    rospy.init_node('teleop_comms', anonymous=True) #
    rate = rospy.Rate(1000) # 1000hz to be changed later if needed
    device.open()
    msg = 0
    hex_0x = '0x'

    while not rospy.is_shutdown():
        def data_receive_callback(xbee_message):
            #l_drive = xbee_message.data.decode()
            imcoming = xbee_message.data.decode()

            ####### if data is a set of 32 numbers:::
            vel_mag_str = str(imcoming[0:7])
            x_direc_str = str(imcoming[8:15])
            y_direc_str = str(imcoming[16:23])
            checksum_str = str(imcoming[24:31])

            #The following converts values back to floats
            vel_mag = struct.unpack('!f',vel_mag_str.decode('hex'))[0]
            x_direc = struct.unpack('!f',x_direc_str.decode('hex'))[0]
            y_direc = struct.unpack('!f',y_direc_str.decode('hex'))[0]

            #Now we will check to ensure our packet was sent correctly
            check = float_to_hex(vel_mag + x_direc + y_direc)
            if str(check) == checksum_str:
                Joy_msg.axes[3] = vel_mag
                Joy_msg.axes[1] = y_direc
                Joy_msg.axes[0] = x_direc
                pub.publish(Joy_msg)
            else:
                print('Checksum does not add up.')
            #msg = hexint(l_drive)
            #print(msg)
            #pub.publish(Int16(msg))

        device.add_data_received_callback(data_receive_callback)
        print("Waiting for data...\n")
        #pub.publish(msg)
        rospy.spin()
        rate.sleep() #

	print("*******Closing Device************")
    device.close()

def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
