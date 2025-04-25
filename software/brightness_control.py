#!/usr/bin/python3

from evdev import InputDevice, categorize, ecodes, list_devices
import pigpio
import threading
import time
import atexit
import os

device = False

while device == False:
    devices = [InputDevice(path) for path in list_devices()]
    if (len(devices) > 0):
        device_path = devices[0].path
        device = InputDevice(device_path)
    time.sleep(1)

file_path = "/etc/brightness.txt"
pin_backlight = 24
brightness_max = 100
brightness_step = 2
current_brightness = brightness_max
adjusting = False
timestep_initial = 0.5
timestep_fast = 0.08
timestep = timestep_initial

if os.path.exists(file_path):
    with open(file_path, "r") as f:
        current_brightness = int(f.read())

pi = pigpio.pi()
pi.set_mode(pin_backlight, pigpio.OUTPUT)
pi.set_PWM_range(pin_backlight, brightness_max)
pi.set_PWM_frequency(pin_backlight, 800)
pi.set_PWM_dutycycle(pin_backlight, max(current_brightness * current_brightness // brightness_max, 1))

def adjust_brightness(first, delta):
    global current_brightness, adjusting, timestep
    if first == True:
        adjusting = True
        timestep = timestep_initial
    if adjusting == False:
        return
    current_brightness += delta
    if current_brightness < brightness_step:
        current_brightness = brightness_step
    elif current_brightness > brightness_max:
        current_brightness = brightness_max
    pi.set_PWM_dutycycle(pin_backlight, max(current_brightness * current_brightness // brightness_max, 1))
    timer = threading.Timer(timestep, adjust_brightness, [False, delta])
    if timestep == timestep_initial:
        timestep = timestep_fast
    timer.start()

def save():
    with open(file_path, "w") as f:
        f.write(str(current_brightness))

atexit.register(save)

hotkey_state = 0

for event in device.read_loop():
    if event.type == ecodes.EV_KEY:
        key_event = categorize(event)
        if hotkey_state == key_event.key_down and key_event.keystate == key_event.key_down:
            if event.code == ecodes.BTN_TL2:
                adjust_brightness(True, -brightness_step)
            elif event.code == ecodes.BTN_TR2:
                adjust_brightness(True, brightness_step)
        if event.code in [ecodes.BTN_TRIGGER_HAPPY2, ecodes.BTN_TL2, ecodes.BTN_TR2] and key_event.keystate == key_event.key_up:
            adjusting = False
        if event.code == ecodes.BTN_TRIGGER_HAPPY2:
            hotkey_state = key_event.keystate


