# README for PI Tower Lamp
Controlling a circuit of rgb leds in a lamp to show average color of the windows in the Telefonplan Tower from a webcam image using a RaspberryPI and Python. When a significant change of the average color happens the lamp animates to the new color. Also runs a simulation of lamp color, input colors and enhanced webcam image for testing purposes.

### Tests
Run tests with this command:
`python -m unittest tests`

### Running it
The program can be run in visual mode for developing and debugging and in rgbled mode to control rgb leds.

####On pi in ~/pi_tower_lamp:
`./../env/bin/python main.py --mode rgbled > log.txt`

####For developing:
`python main.py --mode visual`

### Dependencies
Python 2.7, pillow, fabric, fabtools, git-archive-all, rpi.gpio, git, pi-blaster, requests

## EXTRA: Installing your raspi to work with PI Tower lamp using a Mac
Go to http://www.raspberrypi.org/downloads and download the most recent raspbian image.

To set up your SD card, I followed these steps:
http://alltheware.wordpress.com/2012/12/11/easiest-way-sd-card-setup/

Insert the card, plugin an ethernet cable. Power on the raspi and wait a few seconds.

Find the raspi in your network. Go to terminal and input:
`nmap 192.168.1.1/24`

Nmap can take a few minutes. Download from http://nmap.org/download.html#macosx

There are probably many devices in your network. If one device has port 22 open only it's probably the raspi.

Go to terminal and input with the ip you found:
`ssh pi@192.168.1.2`
password: raspberry

Update and config the raspi:
`sudo apt-get update`

`sudo apt-get upgrade`

`sudo raspi-config`

I choose to fill the SD card.

Install and setup your wifi:
https://www.modmypi.com/blog/how-to-set-up-the-ralink-rt5370-wifi-dongle-on-raspian

Then for convenience, setup key based auth:

On the raspi:
`cd ~`

`mkdir .ssh`

`chmod 700 .ssh`


On your mac:
`scp ~/.ssh/id_rsa.pub pi@192.168.1.8:~/.ssh/authorized_keys`

On your raspi again:
`chmod 600 .ssh/authorized_keys`

Clone this repo to your mac and in that directory, run fabfile to provision raspi:
`fab -R pi provision`