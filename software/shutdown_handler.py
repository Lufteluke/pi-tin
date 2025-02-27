#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import os
import sys

pin_button = 7
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_button, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def main():
    while (True):
        if GPIO.input(pin_button):
            time.sleep(1)
            if GPIO.input(pin_button):
                os.system("shutdown now -h")
        time.sleep(1)

if __name__ == "__main__":
    main()
    sys.exit(0)
