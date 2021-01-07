btsensor.py
===========

This is a Python program that reads accelerometer data from micro:bit's Bluetooth interface using [bluepy](https://github.com/IanHarvey/bluepy).

If you can't connect without root privileges, you might have to add special capabilities to `bluepy-helper` program (which handles the communication for `bluepy`):

```
setcap cap_net_raw,cap_net_admin+eip bluepy-helper
```
