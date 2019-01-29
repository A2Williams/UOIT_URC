## Here is a package for integrating the DIGI XBEE SX RF 1 Watt Modem to any remote computer.
The goal is to create a ROS package that forms a serial connection between two xbee sx rf modems such that some information about the robot can be shared to a base computer.

Once the package is compiled, you can run the transmitter via:

```
rosrun xbee_sx_rf xbee_broadcast.py
```

And the receiver via:

```
rosrun xbee_sx_rf xbee_receiver.py
```
