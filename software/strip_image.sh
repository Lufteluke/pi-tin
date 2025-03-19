#!/bin/bash
sudo rm /etc/wpa_supplicant/wpa_supplicant.conf
history -c   # Clears the history for the current session
history -w   # Writes the changes to the history file
sudo rm ~/.bash_history  # Removes the history file
sudo killall emulationstation
sudo rm .emulationstation/es_input.cfg.bak
sudo rm .emulationstation/es_input.cfg
sudo rm .emulationstation/es_temporaryinput.cfg
sudo rm .emulationstation/es_log.txt
sudo rm .emulationstation/es_log.txt.bak
