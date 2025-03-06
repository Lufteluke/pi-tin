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
            time.sleep(0.3)
            if GPIO.input(pin_button):
                # stop retroarch first to allow it to save state
                os.system("killall -s SIGTERM retroarch")
                time.sleep(0.5)
                os.system("shutdown now -h")
        time.sleep(0.3)

if __name__ == "__main__":
    main()
    sys.exit(0)
