#!/bin/sh
raspi-gpio set 20 ip pu
/usr/bin/python3 /usr/bin/shutdown_handler.py
