## How to initialize 900 MHz communication protocol:

### On Base Computer

Make sure ```roscore``` is running.

Attatch the joystick to one of the USB ports of the base computer.

Run the joystick node by entering:

```
rosrun joy joy_node
```

If it throws up an error, we likely need to change to the location of the joystick in the joystick node. The joystick should show up in the /dev/input/jsX directory, where X is a number (usually 0 or 1). Once you have determined the location, run:

```
rosparam set joy_node/dev "/dev/input/jsX"
```

Again where X is a number.

Once the joystick node is up and running, plug in one of the Digi Xbee Modems to the computer through a USB to USB Mini B cable and run:

```
rosrun xbee-sx-rf xbee_broadcast.py 
```

If this throws up an error, you may have to change the serial ports of two files. They are located:

```
/UOIT_URC/src/xbee-sx-rf/src/xbee_broadcast.py
/UOIT_URC/src/xbee-sx-rf/src/digi/xbee/devices.py
```

You may have to change "/dev/ttyUSB0" in both of the above files to whichever port the Modem is connected to.

This should run just fine. If it doesnt, fix it.

This node converts some values from the /joy topic to hex for sending over RF.

### On the Jetson

Make sure ```roscore``` is running.

Plug in the Modem to one of the USB ports on the Jetson

Run the following to set up the RF receiver.
```
rosrun xbee-sx-rf xbee_receiver.py 
```
If this throws up an error, try changing the port (same way as base).

This node should take in the values from the modem and publish to /joy, as if the joystick was directly connected to the Rover.


