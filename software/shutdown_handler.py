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
            time.sleep(0.5)
            if GPIO.input(pin_button):
                os.system("echo 1 >/sys/class/leds/led0/brightness")
                # stop retroarch first to allow it to save state
                os.system("killall -s SIGTERM retroarch")
                os.system("killall -s SIGTERM emulationstatio")
                os.system("killall -s SIGTERM emulationstation")
                time.sleep(3)
                # stop gpionext (if this is not done it can cause system to hang for 2 minutes before shutdown if a button is held down at shutdown time)
                os.system("systemctl kill gpionext")
                # stop pigpiod (if this is not done it can cause system to randomly hang before shutdown)
                os.system("killall -s SIGKILL pigpiod")
                time.sleep(0.5)
                os.system("shutdown now -h")
        time.sleep(0.3)

if __name__ == "__main__":
    main()
    sys.exit(0)
