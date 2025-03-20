# Pi Tin Full Software Installation Guide

To install and configure all required software "from scratch" on top of a clean install of RetroPie, follow the instructions below.

## 1. install RetroPie

Download the latest RetroPie image for Raspberry Pi 2/3/Zero 2 W [here](https://retropie.org.uk/download/). Extract the image from the .gz file and write it to a 8GB or larger MicroSD card using [Raspberry Pi Imager](https://www.raspberrypi.com/software/), [Etcher](https://etcher.balena.io/), or [Win32DiskImager](https://sourceforge.net/projects/win32diskimager/).

## 2. set up wifi and ssh for headless operation

After writing the SD card, eject and reinsert it to access the newly created boot partition. Create a file called `wpa_supplicant.conf` in the root directory of the boot partition with the contents below, replacing `SSID` and `PASSWORD` with your network name and password. You can add multiple networks by copying the `network={}` block. If you are outside of the United States, change `country=US` to your country's [ISO two-letter country code](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes).

`wpa_supplicant.conf`

```conf
country=US
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

# RETROPIE CONFIG START
network={
    ssid="SSID"
    psk="PASSWORD"
}
# RETROPIE CONFIG END
```

Create an empty file called `ssh` or `ssh.txt` in the boot partition to enable SSH.

## 3. disable serial console

Edit `cmdline.txt` in the boot partition and remove `console=serial0,115200`. This will disable the hardware serial console, which is necessary since one of the serial pins is used for a gamepad button.

## 4. configure firmware options

Edit `config.txt` in the boot partition and add the content below to the end of the file.

```conf
# Enable GPIO power button functionality
dtoverlay=gpio-shutdown,gpio_pin=7,active_low=0,gpio_pull=up
dtoverlay=gpio-poweroff,gpiopin=3,active_low=1

# Lower GPU memory allocation
gpu_mem=128

# Disable UART
enable_uart=0

# Enable SPI with one chip select line (allow use of GPIO7)
dtoverlay=spi0-1cs,no_miso
```

## 5. connect via SSH

Insert the SD card and power up the Raspberry Pi. If the previous steps were done correctly, it should automatically connect to your WiFi network and you should be able to log in via SSH (`ssh pi@retropie.local`) using the default password `raspberry`.

We strongly recommend changing the user password since SSH and SMB are enabled. This can be done by running the `passwd` command on the Raspberry Pi.

## 6. configure startup behavior

Run the following commands to download the startup script and shutdown button handler and configure them to run at boot, before the GPIOnext service starts.

```shell
sudo curl -o /usr/bin/shutdown_handler.py https://raw.githubusercontent.com/jackw01/pi-tin/main/software/shutdown_handler.py
sudo curl -o /usr/bin/pi_tin_startup.sh https://raw.githubusercontent.com/jackw01/pi-tin/main/software/pi_tin_startup.sh
sudo curl -o /etc/systemd/system/pi_tin_startup.service https://raw.githubusercontent.com/jackw01/pi-tin/main/software/pi_tin_startup.service
sudo chmod +x /usr/bin/shutdown_handler.py
sudo chmod +x /usr/bin/pi_tin_startup.sh
sudo systemctl daemon-reload
sudo systemctl enable pi_tin_startup
sudo systemctl start pi_tin_startup
```

Run the following command to disable waiting for a network connection at boot.
```shell
sudo raspi-config nonint do_boot_wait 1
```

## 7. set up display

Use Adafruit's setup script to install and configure fbcp for the ILI9341 2.8" TFT display. Select the `Cupcade (horizontal screen)`option.

```shell
cd ~
curl -O https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/pitft-fbcp.sh
sudo bash pitft-fbcp.sh
```

## 8. set up audio

Use Adafruit's setup script to MAX98357 I2S DAC. **Do not** enable the option to activate /dev/zero playback in the background.

```shell
cd ~
sudo apt-get update
sudo apt-get install python3-pip
pip3 install adafruit-python-shell
curl -O https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/main/i2samp.py
sudo -E env PATH=$PATH python3 i2samp.py
```

Edit `/boot/config.txt` to change the line `dtoverlay=max98357a` to `dtoverlay=max98357a,no-sdmode=on` and change the line `dtparam=audio=on` to `#dtparam=audio=on`.

After rebooting, run `speaker-test -c2`. You should hear white noise from the speaker.

## 9. set up gamepad driver

Clone our fork of [GPIONext](https://github.com/jackw01/GPIOnext) (this fork supports using certain GPIO pins that the original does not) and download the config file. Run the install script and enter `n` when asked to run the configuration manager, then start the GPIOnext daemon. The EmulationStation UI should now respond to button presses.

```shell
cd ~
git clone https://github.com/jackw01/GPIOnext.git
curl -o GPIOnext/config/config.db https://raw.githubusercontent.com/jackw01/pi-tin/main/software/config.db
bash GPIOnext/install.sh
gpionext start
```

## 10. update RetroPie and OS packages

Run the RetroPie setup script.

```shell
sudo ~/RetroPie-Setup/retropie_setup.sh
```

Follow the prompts and select `Update` to update installed packages. Select `Yes` on the prompt asking to update OS packages. This will take a while.

## 11. install RetroPie theme

To install a theme that works better on small displays, first run the RetroPie setup script.

```shell
sudo ~/RetroPie-Setup/retropie_setup.sh
```

Select `Configuration / Tools > esthemes > Install anthonycaccese/tft`. Exit the setup script. Run the command below to create the EmulationStation settings file, which shouldn't exist yet, and set the theme to `tft`.

```shell
cd ~
curl -o .emulationstation/es_settings.cfg https://raw.githubusercontent.com/jackw01/pi-tin/main/software/es_settings.cfg
```

## 12. configure RetroArch

For more seamless operation, we recommend configuring RetroArch to automatically save the game state when exiting and load the saved state when starting. This setting can be changed later for individual ROMs. To do this, edit `/opt/retropie/configs/all/retroarch.cfg` and change the lines

```conf
savestate_auto_load = ...
savestate_auto_save = ...
```

to

```conf
savestate_auto_load = "true"
savestate_auto_save = "true"
```

When combined with the Pi Tin shutdown handler script, this change will allow the state to be automatically saved before the system shuts down.

## 13. set volume

Run `amixer set PCM 50%` to set the volume to a more reasonable level.

## additional notes

For now, do not install `pulseaudio` to use Bluetooth audio devices. In testing we found that it interacts poorly with the MAX98357 I2S DAC+amp and causes it to draw so much current that it triggers the battery protection circuit.

## sources

- [Running OpenGL-based Games & Emulators on Adafruit PiTFT Displays](https://learn.adafruit.com/running-opengl-based-games-and-emulators-on-adafruit-pitft-displays/)
- [Adafruit MAX98357 I2S Class-D Mono Amp](https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/overview)
