# Software Setup

## 1. install RetroPie

Download the latest RetroPie pre-made image for Raspberry Pi 2/3/Zero 2 W [here](https://retropie.org.uk/download/). Extract the image from the .gz file and write it to a 8GB or larger MicroSD card using [Raspberry Pi Imager](https://www.raspberrypi.com/software/), [Etcher](https://etcher.balena.io/), or [Win32DiskImager](https://sourceforge.net/projects/win32diskimager/).

## 2. set up wifi and ssh for headless operation

After writing the SD card, eject and reinsert it to access the newly created boot partition. Create a file called `wpa_supplicant.conf` in the root directory of the boot partition with the contents below, replacing `SSID` and `PASSWORD` with your network name and password. If you are outside of the United States, change `country=US` to your country's [ISO two-letter country code](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes).

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

## 4. disable serial console

Edit `cmdline.txt` in the boot partition and remove `console=serial0,115200`. This will disable the hardware serial console, which is necessary since one of the serial pins is used for a gamepad button.

## 5. configure firmware options

Edit `config.txt` in the boot partition and add the content below to the end of the file.

```txt
# Enable GPIO power button functionality
dtoverlay=gpio-shutdown,gpio_pin=7,active_low=0,gpio_pull=up
dtoverlay=gpio-poweroff,gpiopin=3,active_low=1

# Lower GPU memory allocation
gpu_mem=128

# Enable SPI with one chip select line (allow use of GPIO7)
dtoverlay=spi0-1cs,no_miso
```

## 6. boot raspberry pi

Insert the SD card and power up the Raspberry Pi. If the previous steps were done correctly, it should automatically connect to your WiFi network and you should be able to log in via SSH (`ssh pi@retropie.local`) using the default password `raspberry`.

## set up startup script

```txt
curl https://raw.githubusercontent.com/jackw01/pi-tin/main/software/shutdown_handler.py > /usr/bin/shutdown_handler.py
curl https://raw.githubusercontent.com/jackw01/pi-tin/main/software/pi_tin_startup.sh > /usr/bin/pi_tin_startup.sh
curl https://raw.githubusercontent.com/jackw01/pi-tin/main/software/pi_tin_startup.service > /etc/systemd/system/pi_tin_startup.service
sudo chmod +x /usr/bin/shutdown_handler.py
sudo chmod +x /usr/bin/pi_tin_startup.sh
sudo systemctl daemon-reload
sudo systemctl enable pi_tin_startup
sudo systemctl start pi_tin_startup
```

## set up display

Use Adafruit's setup script to install and configure fbcp for the ILI9341 2.8" TFT display. Select the PiGRRL 2 option.

```txt
cd ~
curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/pitft-fbcp.sh > pitft-fbcp.sh
sudo bash pitft-fbcp.sh
```

## set up audio

Use Adafruit's setup script to MAX98357 I2S DAC. **Do not** enable the option to activate /dev/zero playback in the background.

```txt
cd ~
pip3 install adafruit-python-shell
curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/main/i2samp.py > i2samp.py
sudo -E env PATH=$PATH python3 i2samp.py
```

After rebooting, run `speaker-test -c2`. You should hear white noise from the speaker.

## set up gamepad driver

// copy gpionext config



```txt
cd ~
git clone https://github.com/jackw01/GPIOnext.git
bash GPIOnext/install.sh
```

## set up gamepad in RetroPie

## update RetroPie

https://retropie.org.uk/docs/Updating-RetroPie/#:~:text=The%20conventional%20way%20to%20update,%2DSetup%2Fretropie_setup.sh%20.

## change RetroPie theme


### sources
- [Running OpenGL-based Games & Emulators on Adafruit PiTFT Displays](https://learn.adafruit.com/running-opengl-based-games-and-emulators-on-adafruit-pitft-displays/)
- [Adafruit MAX98357 I2S Class-D Mono Amp](https://learn.adafruit.com/adafruit-max98357-i2s-class-d-mono-amp/overview)
