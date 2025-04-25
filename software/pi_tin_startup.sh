#!/bin/sh
echo 0 | tee /sys/class/leds/led0/brightness
raspi-gpio set 20 ip pu
pigpiod -m -t 0
/usr/bin/python3 /usr/bin/shutdown_handler.py &
/usr/bin/python3 /usr/bin/brightness_control.py &
